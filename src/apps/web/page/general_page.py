from selenium.webdriver.common.by import By

from src.consts import DISPLAY_TIMEOUT
from src.utils import logger
from src.utils.element_util import WebActions


class GeneralPage:

    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __ic_loading = (By.CSS_SELECTOR, "div.loader, div[data-testid='spin-loader']")

    def wait_for_loading_complete(self, timeout=DISPLAY_TIMEOUT):
        self.actions.wait_for_condition(
            lambda: len(
                self.actions.find_elements(self.__ic_loading, visible=False, show_log=False, timeout=timeout)
            ) == 0
        )
