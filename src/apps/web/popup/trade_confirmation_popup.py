from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class TradeConfirmationPopup:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __btn_confirm = (By.CSS_SELECTOR, "button[data-testid='trade-confirmation-button-confirm']")
    __lbl_confirmation_order_side = (By.CSS_SELECTOR, "div[data-testid='trade-confirmation-order-type'")
    __lbl_confirmation_symbol = (By.CSS_SELECTOR, "div[data-testid='trade-confirmation-symbol'")
    __lbl_confirmation_value_list = (By.CSS_SELECTOR, "div[data-testid='trade-confirmation-value'")

    def get_confirmation_symbol(self):
        return self.actions.get_text(self.__lbl_confirmation_symbol).strip()

    def get_confirmation_trade_order_info(self, is_volume_size=False) -> list:
        """
        return: a list of trade order information in the following order
            [order side, volume, stop loss, take profit]
        """
        trade_order_info = [
            self.actions.get_text(self.__lbl_confirmation_order_side).capitalize(),
            *self.actions.get_list_text(self.__lbl_confirmation_value_list)
        ]
        pop_index = 1 if is_volume_size else 2
        trade_order_info.pop(pop_index)
        return trade_order_info

    def confirm(self):
        self.actions.click(self.__btn_confirm)
