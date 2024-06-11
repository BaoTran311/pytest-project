from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from src.page_object.general import GeneralPage


class LoginPage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)

    __txt_username = (By.NAME, "sign_username__")
    __txt_password = (By.NAME, "sign_passwd__")
    __btn_login = (By.XPATH, "//button[text()='Sign In']")

    def login(self, username, password):
        # if self.actions.is_displayed(self.__txt_username):
        self.actions.send_keys(self.__txt_username, username, press=Keys.TAB)
        self.actions.send_keys(self.__txt_password, password, press=Keys.TAB)
        self.actions.click(self.__btn_login)
