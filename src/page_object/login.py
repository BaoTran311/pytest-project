from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from src.page_object.general import GeneralPage


class LoginPage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)

    __txt_username = (By.NAME, "sign_username__")
    __txt_password = (By.NAME, "sign_passwd__")
    __btn_login = (By.XPATH, "//button[text()='Sign In']")
    __txt_error = (By.CSS_SELECTOR, "#LoginForm .error-text")

    def login(self, username, password):
        self.logger.debug(f"Account: {username} - {password}")
        self.actions.send_keys(self.__txt_username, username, press=Keys.TAB)
        self.actions.send_keys(self.__txt_password, password, press=Keys.TAB)
        self.actions.click(self.__btn_login)

    def get_error_text(self):
        return self.actions.get_text(self.__txt_error)

    def verify_error_text_is_displayed_with_correct_content(self, content):
        assert self.get_error_text() == content
