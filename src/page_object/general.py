from src.utils import logger
from src.utils.element_util import ActionsElement


class GeneralPage:

    def __init__(self, driver=None):
        self.actions = ActionsElement(driver)
        self.logger = logger
