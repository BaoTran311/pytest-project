import builtins

from src.data_runtime import DataRuntime
from src.page_object.login import LoginPage


class PageContainer:

    def __init__(self, driver=None):
        self._driver = driver or getattr(builtins, 'list_driver')[0]
        self.login = LoginPage(self._driver)

    def navigate_to_flo_web(self):
        self._driver.get(DataRuntime.config.urls.web)
        return self
