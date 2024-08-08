from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class TopNavigation:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __ic_account = (By.XPATH, "//i[contains(@class, 'icon avatar') and ./ancestor::tooltip]")
    __top_nav_bar = (By.XPATH, "//div[contains(@class, 'nav-bar-on-top')]")

    def wait_for_top_navigation_displayed(self):
        self.actions.wait_for_element_visible(self.__top_nav_bar)

    def is_top_navigation_displayed(self):
        return self.actions.is_displayed(self.__top_nav_bar)
