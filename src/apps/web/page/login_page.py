from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from src.apps.web.page.general_page import GeneralPage
from src.data_runtime import DataRuntime
from src.utils.string_util import cook_element


class LoginPage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)

    __tab_dyn = (By.XPATH, "//div[starts-with(@data-testid, 'tab-login-account-type-{}')]")
    __txt_account_id = (By.CSS_SELECTOR, "input[data-testid='login-user-id']")
    __txt_password = (By.CSS_SELECTOR, "input[data-testid='login-password']")
    __btn_signin = (By.CSS_SELECTOR, "button[data-testid='login-submit']")
    __alert_error = (By.CSS_SELECTOR, "div[data-testid='alert-error']")

    def _login(self, account_id, password, tab, wait_completed=False):
        _tab = {i: i for i in ('live', 'demo')}.get(tab)
        self.actions.click(cook_element(self.__tab_dyn, _tab))
        self.actions.send_keys(self.__txt_account_id, account_id, press=Keys.TAB)
        self.actions.send_keys(self.__txt_password, password, press=Keys.TAB)
        self.actions.click(self.__btn_signin)
        if wait_completed:
            self.actions.wait_for_element_not_visible(self.__btn_signin)
            self.wait_for_loading_complete()

    def login_with_demo_account(self, account_id="", password="", *, wait_completed=False):
        account_id = account_id or DataRuntime.config.user
        password = password or DataRuntime.config.password
        self._login(account_id, password, "demo", wait_completed)

    def login_with_live_account(self, account_id, password, *, wait_completed=False):
        self._login(account_id, password, "live", wait_completed)

    def get_alert_error_content(self):
        return self.actions.get_text(self.__alert_error, visible=True).strip()

    def wait_for_login_page_displays(self):
        self.actions.wait_for_element_visible(cook_element(self.__tab_dyn, "demo"))

    def is_alert_error_displayed_with_correct_content(self, content):
        return self.get_alert_error_content() == content
