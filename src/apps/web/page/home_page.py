from selenium.webdriver.common.by import By

from src.apps.web.component.top_navigation import TopNavigation
from src.apps.web.page.general_page import GeneralPage
from src.apps.web.popup.trade_confirmation_popup import TradeConfirmationPopup
from src.enums.side_bar_enum import SideBar
from src.utils import string_util


class HomePage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.top_navigation = TopNavigation(driver)
        self.trade_confirmation_popup = TradeConfirmationPopup(driver)

    __sidebar_dyn = (By.CSS_SELECTOR, "div[data-testid='side-bar-option-{}']")
    __lbl_server_time = (By.XPATH, "//div[@id='root']//span[@dir='ltr']")

    def select_sidebar(self, side_bar: SideBar):
        locator = string_util.cook_element(self.__sidebar_dyn, side_bar.lower())
        self.actions.click(locator)
        self.actions.wait_for_condition(
            lambda: "selected" in self.actions.get_attribute(locator, "class")
        )

    def get_server_time(self):
        return self.actions.get_text(self.__lbl_server_time)
