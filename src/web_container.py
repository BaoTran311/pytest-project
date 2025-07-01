from src.apps.web.page.home_page import HomePage
from src.apps.web.page.login_page import LoginPage
from src.apps.web.page.trade_page import TradePage
from src.data_runtime import DataRuntime


class Web:

    def __init__(self, driver):
        self._driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.trade_page = TradePage(driver)

    def navigate_to_aquariux(self):
        self._driver.get(DataRuntime.config.platforms.web.url)
        self.login_page.wait_for_login_page_displays()

    def refresh_page(self):
        self._driver.refresh()
