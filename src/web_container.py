from src.data_runtime import DataRuntime
from src.page_object.home import HomePage
from src.page_object.login import LoginPage


class WebContainer:

    def __init__(self, driver):
        self._driver = driver
        self.login_page = LoginPage(self._driver)
        self.home_page = HomePage(self._driver)

    def navigate_to_flo_web(self):
        self._driver.get(DataRuntime.config.platforms.web.url)
        return self.login_page
