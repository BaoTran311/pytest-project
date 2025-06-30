import pytest

from src.data_runtime import DataRuntime
from src.mobile_container import Mobile
from src.utils import webdriver_util, appium_util
from src.web_container import Web


@pytest.fixture(scope="module")
def web():
    driver = webdriver_util.init_webdriver(headless=DataRuntime.runtime_option.headless)
    yield Web(driver)
    driver.quit()


@pytest.fixture(scope="package")
def iphone():
    appium_util.init_appium_server("iPhone")
    return Mobile.iphone_container()


@pytest.fixture(scope="package")
def ipad():
    appium_util.init_appium_server("iPad")
    return Mobile.iphone_container()


@pytest.fixture(scope="package", autouse=False)
def mac():
    appium_util.init_appium_server("Mac")
    return Mobile.iphone_container()
