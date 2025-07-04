import pytest

from src.consts import DISPLAY_TIMEOUT
from src.enums.side_bar_enum import SideBar
from src.enums.watch_list_enum import WatchList
from src.utils import webdriver_util, logger
from src.web_container import Web


@pytest.fixture(scope="package")
def web():
    driver = webdriver_util.init_webdriver()
    yield Web(driver)
    driver.quit()


@pytest.fixture(scope="package")
def symbol():
    return "BTCUSD.std"


@pytest.fixture(scope="package", autouse=True)
def navigate_n_login(web):
    logger.info("▶ Precondition:")

    logger.info("\t- Navigate & login to Aquariux")
    web.navigate_to_aquariux()
    web.login_page.login_with_demo_account(wait_completed=True)

    logger.info("\t- Open Trader")
    web.home_page.select_sidebar(SideBar.TRADE)

    logger.info("\t- Select 'All' watchlist")
    web.trade_page.select_watchlist(WatchList.ALL)

    logger.info("\t- Collapse Trade Details")
    web.trade_page.place_order.collapse_trade_details()

    logger.info("\t- Disable One-Click Trading")
    web.trade_page.disable_one_click_trading()
