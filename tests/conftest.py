import builtins
import json
import logging
import time
from contextlib import suppress
from json import JSONDecodeError
from pathlib import Path

import allure
import pytest
import yaml

from src import consts
from src.data_runtime import DataRuntime
from src.utils import logger, create_handler_logger, dotdict, string_util, file_util, datetime_util

_msg_logs = []
_fail_check_point = dict()


def pytest_addoption(parser):
    general = parser.getgroup("General")
    general.addoption("-E", "--env", action="store")
    general.addoption("-D", "--debuglog", action="store_true", default=False)

    support = parser.getgroup("Support")
    support.addoption("--user", action="store", default="", help="Support change user")
    support.addoption("--password", action="store", default="", help="Support generate password")

    project = parser.getgroup("Projects")
    project.addoption("--browser", action="store")
    project.addoption("--headless", action="store_true", default=False)
    parser.addoption("--no_reset", action="store_true", default=False)


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
    path = consts.PROJECT_ROOT / "config" / f"{runtime_option['env']}.yaml"
    with open(path, "r") as _env:
        DataRuntime.config = dotdict(yaml.load(_env, Loader=yaml.FullLoader))
    DataRuntime.runtime_option = dotdict(runtime_option)
    DataRuntime.config.password = string_util.decode(DataRuntime.config.password)

    # switch log level to debug
    if runtime_option["debuglog"]:
        create_handler_logger(logging.DEBUG)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    print("\x00")
    raw_tc_name = item.parent.name.split("_")[1:]
    tc_name = f"{raw_tc_name[0]} - {" ".join(raw_tc_name[1:]).capitalize().replace(".py", "")}"
    parent_suite, *test_suite = item.parent.module.__name__.split(".")[1:-1]  # noqa
    DataRuntime.tc_info = dotdict(name=tc_name, test_suite=test_suite, parent_suite=parent_suite)

    global _fail_check_point
    builtins.fail_check_point[tc_name] = []  # noqa


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
        if report.passed:
            printlog, status = (logger.info, "PASSED")
        elif report.failed:
            printlog, status = (logger.warning, "FAILED")
        printlog("-------------")  # noqa
        printlog(f"Test case   | {test_case_name}")
        printlog(f"Test status | {status} ({datetime_util.pretty_time(report.duration)})")  # noqa
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global _msg_logs

    report = (yield).get_result()
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

        # Log test to allure reports
        for steps in test_steps:
            with allure.step(steps.pop(0)):
                for index, verify in enumerate(steps):
                    with allure.step(verify):
                        if report.failed:
                            for platform, driver in getattr(builtins, "dict_driver").items():
                                attach_name = f"{platform}_{datetime_util.get_current_time(time_format="%d-%Y-%m_%H:%M:%S")}.png"
                                allure.attach(
                                    name=attach_name, body=driver.get_screenshot_as_png(),
                                    attachment_type=allure.attachment_type.PNG,
                                )

        del _msg_logs[:]


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
                        if sub_step['name'] in builtins.fail_check_point[json_obj['name']]:  # noqa
                            sub_step["status"] = "failed"
                            _sub_steps["status"] = "failed"

                        if json_obj['name'] in _fail_tcs_name and \
                                sub_step['name'] not in builtins.fail_check_point[json_obj['name']]:  # noqa
                            del sub_step['attachments']

                # labels - allure report
                # Present, cook (value, name in parentSuite and Suite)
                raw_labels = json_obj["labels"]
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
