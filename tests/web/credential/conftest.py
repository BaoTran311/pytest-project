import pytest

from src.utils import webdriver_util
from src.web_container import Web


@pytest.fixture(scope="module")
def web():
    driver = webdriver_util.init_webdriver()
    yield Web(driver)
    driver.quit()
