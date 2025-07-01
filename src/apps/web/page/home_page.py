from selenium.webdriver.common.by import By

from src.apps.web.component.top_navigation import TopNavigation
from src.apps.web.page.general_page import GeneralPage
from src.enums.side_bar import SideBar
from src.utils import string_util


class HomePage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.top_navigation = TopNavigation(driver)

    __sidebar_dyn = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-{}']")

    # __sidebar_trade = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-trade']")
    # __sidebar_markets = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-markets']")
    # __sidebar_assets = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-assets']")
    # __sidebar_signal = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-signal']")
    # __sidebar_calendar = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-calendar']")
    # __sidebar_news = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-news']")
    # __sidebar_education = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-education']")

    def select_sidebar(self, side_bar: SideBar):
        locator = string_util.cook_element(self.__sidebar_dyn, side_bar.lower())
        self.actions.click(locator)
        self.actions.wait_for_condition(
            lambda: "selected" in self.actions.get_attribute(locator, "class")
        )
