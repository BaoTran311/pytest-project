from src.apps.web.component.top_navigation import TopNavigation
from src.apps.web.page.login import LoginPage
from src.data_runtime import DataRuntime


class Web:

    def __init__(self, driver):
        self._driver = driver
        self.login_page = LoginPage(self._driver)
        self.top_navigation = TopNavigation(self._driver)

    def navigate_to_flo_web(self):
        self._driver.get(DataRuntime.config.platforms.web.url)
        return self.login_page

    def refresh_page(self):
        self._driver.refresh()
