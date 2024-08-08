from src.apps.web.component.item_list.general import GeneralInfobox
from src.utils import logger
from src.utils.element_util import WebActions


class NoteInfobox:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger
