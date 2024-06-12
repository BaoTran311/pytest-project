import pytest

from src.data_runtime import DataRuntime
from src.page_container import PageContainer
from src.utils import webdriver_util


@pytest.fixture(scope="package", autouse=True)
def page():
    driver = webdriver_util.init_webdriver(headless=DataRuntime.runtime_option.headless)
    return PageContainer(driver)
