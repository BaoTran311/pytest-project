import builtins
import json
import logging
import os
import subprocess
import time
from contextlib import suppress
from json import JSONDecodeError
from pathlib import Path

import allure
import pytest
import yaml

from src import consts
from src.consts import PROJECT_ROOT
from src.data_runtime import DataRuntime
from src.utils import logger, create_handler_logger, dotdict, string_util, file_util, datetime_util

_msg_logs = []
_fail_check_point = dict()
VIDEO_NAME = f"{PROJECT_ROOT}/video.mp4"


def pytest_addoption(parser):
    general = parser.getgroup("General")
    general.addoption("-E", "--env", action="store")
    general.addoption("-D", "--debuglog", action="store_true", default=False)

    support = parser.getgroup("Support")
    support.addoption("--user", action="store", default="", help="Support change user")
    support.addoption("--password", action="store", default="", help="Support generate password")
    support.addoption("--record", action="store_true", default=False, help="Support recording test running")
    support.addoption("--remote", action="store_true", default=False, help="Support run test with standalone mode")

    project = parser.getgroup("Projects")
    project.addoption("--browser", action="store")
    project.addoption("--headless", action="store_true", default=False)
    parser.addoption("--no_reset", action="store_true", default=False, help="Run test using current WDA for iOS deivce")


def pytest_sessionstart(session):
    create_handler_logger(logging.INFO)
    setattr(builtins, "dict_driver", dict())
    setattr(builtins, "appium_services", list())
    setattr(builtins, "fail_check_point", dict())

    logger.info("=== Start Pytest session ===")
    runtime_option = vars(session.config.option)

    if runtime_option["collectonly"]:  # count the total number of tests and then exit
        return

    logger.info("Loading config and handle ...")
    path = consts.ENV_DIR / f"{runtime_option['env']}.yaml"
    with open(path, "r") as _env:
        DataRuntime.config = dotdict(yaml.load(_env, Loader=yaml.FullLoader))
    DataRuntime.runtime_option = dotdict(runtime_option)
    DataRuntime.config.password = string_util.decode(DataRuntime.config.password)

    # switch log level to debug
    if runtime_option["debuglog"]:
        create_handler_logger(logging.DEBUG)

    if runtime_option['browser']:
        DataRuntime.config.platforms.web.browser = runtime_option['browser']


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    print("\x00")
    raw_tc_module = item.parent.name.split("_")[1:]
    tc_module = raw_tc_module[0].replace(".py", "")
    tc_name = ' '.join(item.name.replace("test_", "").split("_")).capitalize()
    full_tc_name = f"{tc_module} - {tc_name}"
    parent_suite, *test_suite = item.parent.module.__name__.split(".")[2:-1]  # noqa
    DataRuntime.tc_info = dotdict(name=full_tc_name, test_suite=test_suite, parent_suite=parent_suite)
    # allure.dynamic.testcase(re.sub(r"\bTC(\d+)\b", r"TC-\1", tc_module.upper()), full_tc_name)

    global _fail_check_point
    builtins.fail_check_point[full_tc_name] = []  # noqa


def pytest_runtest_call(item):  # Before each test case
    # print("\x00")  # print a non-printable character to break a new line on console
    ...


def pytest_runtest_teardown(item):  # After each test case
    # print("\x00")  # print a non-printable character to break a new line on console
    tc_name, test_suite, parent_suite = [item for item in DataRuntime.tc_info.values()]  # noqa
    allure.dynamic.parent_suite(parent_suite.capitalize())
    if test_suite:
        allure.dynamic.suite(test_suite[-1].capitalize().replace("_", " "))
    allure.dynamic.title(tc_name)

    global _fail_check_point

    if not builtins.fail_check_point[tc_name]:  # noqa
        del builtins.fail_check_point[tc_name]  # noqa


def pytest_runtest_logreport(report):
    if report.when == "call":
        test_case_name = report.nodeid.split("/")[-1].split(".")[0]
        status = report.outcome
        printlog = logger.info if status == "passed" else logger.warning
        printlog("-------------")  # noqa
        printlog(f"Test case   | {DataRuntime.tc_info.name}")  # noqa
        printlog(f"Test status | {status.upper()} ({datetime_util.pretty_time(report.duration)})")  # noqa
        printlog("-------------")


@pytest.fixture(scope="session", autouse=True)
def auto_allure_logging():
    global _msg_logs

    def patchinfo(f):
        def wrapper(*args, **kwargs):
            *_, _logs = args

            with suppress(Exception):
                # Avoid error _logs is not string
                _msg_log_check = _logs.lower()  # Copy avoid cook data
                _log_msgs_checking = "verify step steps".split()
                if any(_msgs in _msg_log_check for _msgs in _log_msgs_checking):
                    _msg_logs.append(_logs)

            return f(*args, **kwargs)

        return wrapper

    logging.Logger.info = patchinfo(logging.Logger.info)


@pytest.fixture(scope="function", autouse=True)
def record_video():
    if DataRuntime.runtime_option.record and not DataRuntime.runtime_option.headless:
        global VIDEO_NAME
        if os.path.exists(VIDEO_NAME):
            file_util.delete_file(VIDEO_NAME)

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # Overwrite existing file
            "-f", "avfoundation",  # macOS screen capture input
            "-framerate", "15",
            "-i", "1:none",  # Screen index 1, no audio
            "-preset", "ultrafast",
            VIDEO_NAME
        ]
        time.sleep(2)  # Let FFmpeg warm up

        logger.debug("[Recording started]")
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        time.sleep(2)  # Let FFmpeg warm up

    yield  # <-- Your test runs here
    if DataRuntime.runtime_option.record and not DataRuntime.runtime_option.headless:
        logger.debug("[Stopping recording]")
        process.terminate()
        process.communicate()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global _msg_logs, VIDEO_NAME

    report = (yield).get_result()

    if report.when == 'setup' and report.failed:
        for platform, driver in getattr(builtins, "dict_driver").items():
            attach_name = f"setup_{platform}_{datetime_util.get_current_time(time_format="%d-%m-%Y_%H:%M:%S")}.png"
            allure.attach(
                name=attach_name,
                body=driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
    if report.when == "call":
        test_steps = []

        # Find index step in list
        # get description from index
        steps_index = [
            index for index, value in enumerate(_msg_logs)
            if ("step" or "steps" or "Should see") in value.lower()
        ]

        for i in range(len(steps_index)):
            if i == (len(steps_index) - 1):
                test_steps.append(_msg_logs[steps_index[i]:])
                break
            test_steps.append(_msg_logs[steps_index[i]: steps_index[i + 1]])

        fail_check_points = builtins.fail_check_point.get(DataRuntime.tc_info.name, [])
        if not fail_check_points and report.failed:
            for platform, driver in getattr(builtins, "dict_driver").items():
                attach_name = f"{platform}_{datetime_util.get_current_time(time_format="%d-%m-%Y_%H:%M:%S")}.png"
                allure.attach(
                    name=attach_name,
                    body=driver.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )

        # Log test to allure reports
        for steps in test_steps:
            with (allure.step(steps.pop(0))):
                for verify in steps:
                    with allure.step(verify):
                        if report.failed:
                            for item in fail_check_points:
                                if verify in item:
                                    screenshot = item[verify]
                                    allure.attach(
                                        name=screenshot[0],
                                        body=screenshot.pop(-1),
                                        attachment_type=allure.attachment_type.PNG,
                                    )

        del _msg_logs[:]

    if report.when == 'teardown':
        if not os.path.exists(VIDEO_NAME):
            logger.debug("ℹ️ Run with non-record.")
        else:
            logger.debug(f"🎥 Video saved: {VIDEO_NAME}")
            # Attach to Allure
            with open(VIDEO_NAME, "rb") as f:
                allure.attach(body=f.read(), name="Test Recording", attachment_type=allure.attachment_type.MP4)
            file_util.delete_file(VIDEO_NAME)
        if report.failed:
            for platform, driver in getattr(builtins, "dict_driver").items():
                attach_name = f"teardown_{platform}_{datetime_util.get_current_time(time_format="%d-%Y-%m_%H:%M:%S")}.png"
                allure.attach(
                    name=attach_name,
                    body=driver.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )


def pytest_sessionfinish(session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.info("=== End tests session ===")
    logger.info("‣ Quit driver session")

    if vars(session.config.option)["collectonly"]:
        return

    global _fail_check_point
    _fail_tcs_name = [name for name in builtins.fail_check_point.keys()]  # noqa

    if hasattr(builtins, "dict_driver"):
        time.sleep(2)  # Calm down for clean up data,
        for _, driver in getattr(builtins, "dict_driver").items():
            driver.quit()

    if hasattr(builtins, "appium_services"):
        time.sleep(2)  # Calm down for clean up data,
        for service in builtins.appium_services:
            service.stop()

    allure_result_dir = session.config.option.allure_report_dir
    if not allure_result_dir:
        return

    logger.info("‣ Customized allure test results")
    # Delete all .container files
    allure_result_dir = Path(allure_result_dir)
    with open(f"{allure_result_dir}/environment.properties", "w") as f:
        f.write(f"Browser={DataRuntime.config.platforms.web.browser.capitalize()}\n")
        f.write(
            f"Aquariux_TestCases=https://docs.google.com/spreadsheets/d/1TFzYPzAz5Eve0monmAXT7f0oTUfx_GGeGkdeUwLT5bE")
    container_files = allure_result_dir.glob("*-container.json")
    for container_file in container_files:
        file_util.delete_file(container_file)

    # Customize .json files
    result_files = list(allure_result_dir.glob("*-result.json"))
    for result_file in result_files:
        with result_file.open("r", encoding="utf8") as _rf:
            # Avoid error json file from allure generate
            with suppress(JSONDecodeError):
                json_obj = json.load(_rf)

                # Check in steps have failed, and the test case's status has been changed to failed.
                steps = json_obj.get("steps", "")
                for _sub_steps in steps:
                    sub_steps = _sub_steps.get("steps", "")
                    for sub_step in sub_steps:
                        # Loop for sub-steps and change status to failed if checkpoint failed
                        if sub_step['name'] in [
                            list(entry.keys())[0] for entry in builtins.fail_check_point.get(json_obj.get('name'), [])
                        ]:
                            sub_step["status"] = "failed"
                            _sub_steps["status"] = "failed"

                # labels - allure report
                # Present, cook (value, name in parentSuite and Suite)
                raw_labels = json_obj.get("labels")

                json_obj["labels"] = [
                    _label for _label in raw_labels
                    if ("parentSuite" == _label.get('name') or "suite" == _label.get('name'))
                       and _label.get('value').replace(" ", "").istitle()
                ]

                # This test has a bug link causing the test was broken.
                if "links" in json_obj and json_obj["status"] == "broken":
                    json_obj["status"] = "failed"

                # Write the modified json object
                with result_file.open("w") as _f:
                    json.dump(json_obj, _f)
