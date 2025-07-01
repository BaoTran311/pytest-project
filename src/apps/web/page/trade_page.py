from selenium.webdriver.common.by import By

from src.apps.web.component.place_order import PlaceOrder
from src.apps.web.page.home_page import HomePage


class TradePage(HomePage):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.place_order = PlaceOrder(driver)

    __tgl_one_click_trading = (By.XPATH, "//div[starts-with(@data-testid, 'toggle-oct')]")

    def is_one_click_trading_enable(self):
        return "-checked" in self.actions.get_attribute(self.__tgl_one_click_trading, "data-testid")

    def __set_one_click_trading(self, enable: bool):
        if self.is_one_click_trading_enable() != enable:
            self.actions.click(self.__tgl_one_click_trading)
        self.actions.wait_for_condition(
            lambda: self.is_one_click_trading_enable() == enable,
        )

    def enable_one_click_trading(self):
        self.__set_one_click_trading(True)

    def disable_one_click_trading(self):
        self.__set_one_click_trading(False)
