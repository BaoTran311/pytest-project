from src.apps.web.component.top_navigation import TopNavigation
from src.apps.web.page.login import LoginPage
from src.data_runtime import DataRuntime


class Web:

    def __init__(self, driver):
        self._driver = driver
        self.login_page = LoginPage(driver)
        self.top_navigation = TopNavigation(driver)

    def navigate_to_aquariux(self):
        self._driver.get(DataRuntime.config.platforms.web.url)
        self.login_page.wait_for_login_page_displays()

    def refresh_page(self):
        self._driver.refresh()
