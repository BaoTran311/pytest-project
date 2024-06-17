from selenium.webdriver.common.by import By

from src.page_object.general import GeneralPage


class HomePage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)

    __ic_account = (By.XPATH, "//i[contains(@class, 'icon avatar') and ./ancestor::tooltip]")

    def wait_for_homepage_displayed(self):
        self.actions.wait_for_element_visible(self.__ic_account)

    def is_homepage_displays(self):
        return self.actions.is_displayed(self.__ic_account)

    def is_fail(self):
        return False

    def is_pass(self):
        return True
