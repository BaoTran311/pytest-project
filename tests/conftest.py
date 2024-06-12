import builtins
import logging
import time
from contextlib import suppress
from datetime import datetime

import allure
import pytest
import yaml

from src import consts
from src.data_runtime import DataRuntime
from src.utils import logger, create_handler_logger, dotdict, string_util

_msg_logs = []


def pytest_addoption(parser):
    general = parser.getgroup("General")
    general.addoption("-E", "--env", action="store")
    general.addoption("-D", "--debuglog", action="store_true", default=False)

    support = parser.getgroup("Support")
    support.addoption("--user", action="store", default="", help="Support change user")
    support.addoption("--password", action="store", default="", help="Support generate password")

    project = parser.getgroup("Projects")
    # project.addoption("--browser", action="store")
    project.addoption("--headless", action="store_true", default=False)


def pytest_sessionstart(session):
    create_handler_logger(logging.INFO)

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


def pytest_runtest_logreport(report):
    if report.when == "call":
        test_case_name = report.nodeid.split("/")[-1].split(".")[0]
        if report.passed:
            printlog, status = (logger.info, "PASSED")
        elif report.failed:
            printlog, status = (logger.warning, "FAILED")
            for platform, driver in getattr(builtins, "dict_driver").items():
                driver.save_screenshot(f"{platform}_{datetime.now()}.png")
        printlog("-------------")  # noqa
        printlog(f"Test case   | {test_case_name}")
        printlog(f"Test status | {status}")
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
            step = steps.pop(0)
            with allure.step(step):
                for verify in steps:
                    with allure.step(verify):
                        pass

        del _msg_logs[:]


def pytest_sessionfinish(session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.info("=== End tests session ===")
    logger.info("‣ Quit driver session")
    if hasattr(builtins, "dict_driver"):
        time.sleep(2)  # Calm down for clean up data,
        for _, driver in getattr(builtins, "dict_driver").items():
            driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    print("\x00")


# def pytest_runtest_call(item):
#     logger.info("pytest_runtest_call")


# def pytest_runtest_teardown(item):  # After each test case
#     logger.info("pytest_runtest_teardown")
#     print("\x00")  # print a non-printable character to break a new line on console
#     item_location, *_ = item.location

@pytest.fixture(scope="session", name="screen")
def screen_container():
    logger.info("Starting appium driver ...")
    # driver = appium_util.create_driver()
    # setattr(builtins, "dict_driver", {DataRuntime.platforms: driver})
    # return PageContainer(driver)
