import builtins
import logging
import time
from datetime import datetime

import pytest
import yaml

from src import consts
from src.data_runtime import DataRuntime
from src.page_container import PageContainer
from src.utils import logger, webdriver_util, create_handler_logger, dotdict, string_util


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


# def pytest_runtest_teardown(item):  # After each test case
#     logger.info("pytest_runtest_teardown")
#     print("\x00")  # print a non-printable character to break a new line on console
#     item_location, *_ = item.location


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


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     logger.info("pytest_runtest_makereport - before")
#     report = (yield).get_result()
#     logger.info("pytest_runtest_makereport - after")
#     if report.when == "call":
#         # pytest.set_trace()
#         ...
#     # allure.step("asdfasdf")


def pytest_sessionfinish(session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.info("=== End tests session ===")
    logger.info("‣ Quit driver session")
    if hasattr(builtins, "list_driver"):
        time.sleep(2)  # Calm down for clean up data,
        for driver in getattr(builtins, "list_driver"):
            driver.quit()


# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_setup(item: pytest.Item):
#     print("\x00")
#     logger.info("pytest_runtest_setup")
#
#
# def pytest_runtest_call(item):
#     logger.info("pytest_runtest_call")


@pytest.fixture(scope="session", name="page", autouse=True)
def page_manager():
    logger.info("Starting webdriver ...")
    print("\x00")
    driver = webdriver_util.create_chrome_driver(headless=DataRuntime.runtime_option.headless)
    setattr(builtins, "dict_driver", {DataRuntime.config.platforms.web: driver})
    return PageContainer(driver)


@pytest.fixture(scope="session", name="screen")
def screen_container():
    logger.info("Starting appium driver ...")
    # driver = appium_util.create_driver()
    # setattr(builtins, "dict_driver", {DataRuntime.platforms: driver})
    # return PageContainer(driver)
