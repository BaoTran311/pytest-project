import pytest

from src.data_runtime import DataRuntime
from src.page_container import WebContainer
from src.screen_container import iPhoneContainer
from src.utils import webdriver_util, appium_util


@pytest.fixture(scope="package", autouse=True)
def page():
    driver = webdriver_util.init_webdriver(headless=DataRuntime.runtime_option.headless)
    return WebContainer(driver)


@pytest.fixture(scope="package", autouse=True)
def iphone_screen():
    appium_util.init_appium_server("iPhone")
    return iPhoneContainer()
