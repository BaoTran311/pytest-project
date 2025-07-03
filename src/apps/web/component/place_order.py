from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from src.apps.web.popup.trade_confirmation_popup import TradeConfirmationPopup
from src.data_object.trade_order import TradeOrder
from src.enums.place_order import VolumeType
from src.utils import logger, string_util
from src.utils.element_util import WebActions


class PlaceOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger
        self.trade_confirmation_popup = TradeConfirmationPopup(driver)

    __btn_trade_order_type_dyn = (By.CSS_SELECTOR, "div[data-testid='trade-button-order-{}']")
    __lbl_live_buy_price = (By.CSS_SELECTOR, "div[data-testid='trade-live-buy-price']")
    __lbl_live_sell_price = (By.CSS_SELECTOR, "div[data-testid='trade-live-sell-price']")
    __pnl_trade_detail_status = (
        By.XPATH, "//div[./parent::div[@data-testid='trade-details'] and .//span[@aria-expanded]]"
    )
    __tgl_swap_volume = (By.XPATH, "//div[starts-with(@data-testid, 'trade-swap-to')]")
    __txt_trade_volume = (By.CSS_SELECTOR, "input[data-testid='trade-input-volume']")
    __txt_trade_stop_loss_price = (By.CSS_SELECTOR, "input[data-testid='trade-input-stoploss-price']")
    __txt_trade_take_profit_price = (By.CSS_SELECTOR, "input[data-testid='trade-input-takeprofit-price']")
    __btn_place_buy_or_sell_order = (By.CSS_SELECTOR, "button[data-testid='trade-button-order']")

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
        # self.actions.wait_for_condition(
        #     lambda: VolumeType.__dict__.get(self.get_current_volume_type().upper(), "volume") != volume_type
        # )

    def switch_to_units(self):
        self.__set_volume(VolumeType.UNITS)

    def switch_to_size(self):
        self.__set_volume(VolumeType.SIZE)

    def place_an_order(self, trade_order: TradeOrder, confirm=True):
        # Select Buy or Sell
        trade_locator = string_util.cook_element(self.__btn_trade_order_type_dyn, trade_order.order_side.lower())
        self.actions.click(trade_locator)

        # Select Units or Size
        self.switch_to_size() if trade_order.is_volume_size() else self.switch_to_units()

        # Fill place order information
        self.actions.send_keys(self.__txt_trade_volume, trade_order.get_volume_value())
        self.actions.send_keys(self.__txt_trade_stop_loss_price, trade_order.stop_loss, press=Keys.TAB)
        self.actions.send_keys(self.__txt_trade_take_profit_price, trade_order.take_profit, press=Keys.TAB)

        # Click Place Buy/Sell Order
        self.actions.click(self.__btn_place_buy_or_sell_order)

        if confirm:
            self.trade_confirmation_popup.confirm()
