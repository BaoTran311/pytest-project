from selenium.webdriver.common.by import By

from src.enums.order_enum import AssetOrderType
from src.utils import logger
from src.utils.element_util import WebActions
from src.utils.string_util import cook_element


class AssetOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __tab_asset_order_type_dyn = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-{}']")

    def select_asset_order(self, asset_order_type: AssetOrderType):
        locator = cook_element(self.__tab_asset_order_type_dyn, "")

    def wait_for_top_navigation_displays(self):
        self.actions.wait_for_element_visible(self.__btn_setting)

    def is_setting_button_displayed(self):
        return self.actions.is_displayed(self.__btn_setting)

    def is_switch_theme_button_displayed(self):
        return self.actions.is_displayed(self.__btn_switch_theme)

    def is_notification_button_displayed(self):
        return self.actions.is_displayed(self.__btn_notification)
