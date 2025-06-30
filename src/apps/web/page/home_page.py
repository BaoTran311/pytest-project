from src.apps.web.component.top_navigation import TopNavigation
from src.apps.web.page.general_page import GeneralPage


class HomePage(GeneralPage):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.top_navigation = TopNavigation(driver)
