from selenium.webdriver.common.by import By

from src.enums.order_enum import AssetOrderType
from src.utils import logger
from src.utils.element_util import WebActions
from src.utils.string_util import cook_element


class _AssetColumnProperty:
    OPEN_DATE = "open-date"
    CLOSE_DATE = "close-date"
    ORDER_ID = "order-id"
    STATUS = "status"
    ORDER_TYPE = "order-type"
    PROFIT = "profit"
    SIZE = "volume"
    UNITS = "Units"
    ENTRY_PRICE = "entry-price"
    CURRENT_PRICE = "current-price"
    TAKE_PROFIT = "take-profit"
    STOP_LOSS = "stop-loss"
    SWAP = "swap"
    COMMISSION = "commission"
    REMARKS = "remarks"


class AssetOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __tab_open_position = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-open-positions']")
    __tab_pending_orders = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-pending-orders']")
    __tab_order_history = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-history']")
    __lbl_asset_open_column_dyn = (By.CSS_SELECTOR, "td[data-testid='asset-open-column-{}']")
    __lbl_asset_history_column_dyn = (By.CSS_SELECTOR, "td[data-testid='asset-history-column-{}']")

    def select_asset_order(self, asset_order_type: AssetOrderType):
        locator = {
            AssetOrderType.PENDING_ORDERS: self.__tab_pending_orders,
            AssetOrderType.ORDER_HISTORY: self.__tab_order_history,
            AssetOrderType.OPEN_POSITIONS: self.__tab_open_position,
        }.get(asset_order_type)  # noqa
        self.actions.click(locator)

    def __get_row_value_based_on_column(self, asset_order_type: AssetOrderType, asset_property):
        root_locator = {
            AssetOrderType.PENDING_ORDERS: "",
            AssetOrderType.ORDER_HISTORY: self.__lbl_asset_history_column_dyn,
            AssetOrderType.OPEN_POSITIONS: self.__lbl_asset_open_column_dyn,
        }.get(asset_order_type)  # noqa
        locator = cook_element(root_locator, asset_property)
        return self.actions.get_text(locator)

    def get_open_date(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.OPEN_DATE)

    def get_type(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.ORDER_TYPE)

    def get_take_profit(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.TAKE_PROFIT)

    def get_units(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.UNITS)

    def get_size(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.SIZE)

    # def get_stop_loss