from selenium.webdriver.common.by import By

from src.page_object.general import GeneralPage


class HomePage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)

    __ic_account = (By.XPATH, "//i[contains(@class, 'icon avatar') and ./ancestor::tooltip]")

    def verify_homepage_displays(self):
        assert self.actions.is_displayed(self.__ic_account)
