from selenium.webdriver.common.by import By

from src.enums.place_order import VolumeType
from src.utils import logger
from src.utils.element_util import WebActions


class PlaceOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __btn_buy = (By.CSS_SELECTOR, "div[data-testid='trade-button-order-buy']")
    __lbl_live_buy_price = (By.CSS_SELECTOR, "div[data-testid='trade-live-buy-price']")
    __btn_sell = (By.CSS_SELECTOR, "div[data-testid='trade-button-order-sell']")
    __lbl_live_sell_price = (By.CSS_SELECTOR, "div[data-testid='trade-live-sell-price']")
    __pnl_trade_detail_status = (
        By.XPATH, "//div[./parent::div[@data-testid='trade-details'] and .//span[@aria-expanded]]"
    )
    __tgl_swap_volume = (By.XPATH, "//div[starts-with(@data-testid, 'trade-swap-to')]")
    __btn_trade_volume_increase = (By.CSS_SELECTOR, "div[data-testid='trade-input-volume-increase']")
    __btn_trade_volume_decrease = (By.CSS_SELECTOR, "div[data-testid='trade-input-volume-decrease']")

    def get_live_buy_price(self):
        return self.actions.get_text(self.__lbl_live_buy_price).strip()

    def is_trade_details_expanded(self):
        return "expanded" in self.actions.get_attribute(self.__pnl_trade_detail_status, "class")

    def __set_trade_details(self, expanded):
        if self.is_trade_details_expanded() != expanded:
            self.actions.click(self.__pnl_trade_detail_status)
        self.actions.wait_for_condition(
            lambda: self.is_trade_details_expanded() == expanded
        )

    def expand_trade_details(self):
        self.__set_trade_details(True)

    def collapse_trade_details(self):
        self.__set_trade_details(False)

    def get_current_volume_type(self):
        return self.actions.get_attribute(self.__tgl_swap_volume, "data-testid").split("-")[-1]

    def __set_volume(self, volume_type):
        current_volume = VolumeType.__dict__.get(self.get_current_volume_type().upper(), "volume")
        volume_type = volume_type if volume_type == VolumeType.UNITS else "volume"
        if current_volume == volume_type:
            self.actions.click(self.__tgl_swap_volume)
        self.actions.wait_for_condition(
            lambda: VolumeType.__dict__.get(self.get_current_volume_type().upper(), "volume") != volume_type
        )

    def swap_to_units(self):
        self.__set_volume(VolumeType.UNITS)

    def swap_to_size(self):
        self.__set_volume(VolumeType.SIZE)
