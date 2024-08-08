import pytest

from src.data_runtime import DataRuntime
from src.web_container import Web
from src.mobile_container import Mobile
from src.utils import webdriver_util, appium_util


@pytest.fixture(scope="package", autouse=False)
def web():
    driver = webdriver_util.init_webdriver(headless=DataRuntime.runtime_option.headless)
    return Web(driver)


@pytest.fixture(scope="package", autouse=False)
def iphone():
    appium_util.init_appium_server("iPhone")
    return Mobile.iphone_container()
