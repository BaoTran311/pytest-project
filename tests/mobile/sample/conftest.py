import pytest

from src.mobile_container import Mobile
from src.utils import appium_util


@pytest.fixture(scope="package")
def iphone():
    appium_util.init_appium_server("iPhone")
    return Mobile.iphone_container()
