import pytest

from src.data_runtime import DataRuntime
from src.web_container import WebContainer
from src.mobile_container import MobileContainer
from src.utils import webdriver_util, appium_util


@pytest.fixture(scope="package", autouse=False)
def flo_web():
    driver = webdriver_util.init_webdriver(headless=DataRuntime.runtime_option.headless)
    return WebContainer(driver)


@pytest.fixture(scope="package", autouse=False)
def flo_iphone():
    appium_util.init_appium_server("iPhone")
    return MobileContainer.iphone_container()
