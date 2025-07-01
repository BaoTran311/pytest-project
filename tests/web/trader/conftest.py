import pytest

from src.enums.side_bar import SideBar
from src.utils import webdriver_util, logger
from src.web_container import Web


@pytest.fixture(scope="package")
def web():
    driver = webdriver_util.init_webdriver()
    yield Web(driver)
    driver.quit()


@pytest.fixture(scope="package", autouse=True)
def navigate_n_login(web):
    logger.info("▶ Precondition: \n")

    logger.info("Navigate & login to Aquariux")
    web.navigate_to_aquariux()
    web.login_page.login_with_demo_account(wait_completed=True)

    logger.info("Open Trader")
    web.home_page.select_sidebar(SideBar.TRADE)

    logger.info("Disable One-Click Trading")
    web.trade_page.disable_one_click_trading()

    logger.info("Collapse Trade Details")
    web.trade_page.place_order.collapse_trade_details()
