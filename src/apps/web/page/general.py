from src.apps.web.component.top_navigation import TopNavigation
from src.utils import logger
from src.utils.element_util import WebActions


class GeneralPage:

    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    def refresh(self):
        self.logger.debug("Refresh page")
        self._driver.execute_script("window.onbeforeunload = function() {};")
        self._driver.refresh()
