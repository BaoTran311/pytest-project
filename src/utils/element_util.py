import functools
import logging
from contextlib import suppress

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as exc
from selenium.webdriver.support.wait import WebDriverWait

from src import consts
from src.consts import TIMEOUT, DISPLAY_TIMEOUT

_logger = logging.getLogger(consts.PYTHON_CONFIG)


class Actions:
    def __init__(self, driver):
        self._driver = driver
        self._action_chains = ActionChains(self._driver)

    def __wait_for_element__(self, element: tuple, /, *, func=None, timeout=TIMEOUT):
        webdriver_wait = WebDriverWait(self._driver, timeout)
        return webdriver_wait.until(func(element))

    wait_for_element_visible = functools.partialmethod(__wait_for_element__, func=exc.visibility_of_element_located)
    wait_for_element_not_visible = functools.partialmethod(
        __wait_for_element__, func=exc.invisibility_of_element_located
    )
    wait_for_element_presence = functools.partialmethod(__wait_for_element__, func=exc.presence_of_element_located)
    wait_for_element_clickable = functools.partialmethod(__wait_for_element__, func=exc.element_to_be_clickable)

    def find_element(
            self, element: tuple, /,
            *, timeout=TIMEOUT, visible=True, wait=True, show_log=True
    ) -> WebElement:
        with suppress(NoSuchElementException, TimeoutException):
            if wait:
                if visible:
                    return self.wait_for_element_visible(element, timeout=timeout)
                return self.wait_for_element_presence(element, timeout=timeout)
            return self._driver.find_element(*element)

        msg_log = f"Element not found with locator {element[1]!r} after {timeout!r} seconds"
        if show_log:
            _logger.error(msg_log)
        raise NoSuchElementException(msg_log)

    def click(
            self, element: tuple, /,
            *, timeout=TIMEOUT, visible=True, show_log=True
    ):
        self.wait_for_element_clickable(element, timeout=timeout)
        ele = self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
        ele.click()

    def clear_text(self, element: tuple, /, visible=False, timeout=TIMEOUT):
        self.find_element(element, visible=visible, timeout=timeout).clear()

    def send_keys(
            self, element: tuple, text, /,
            *, clear=True, press: Keys = None, visible=True, timeout=TIMEOUT
    ):
        if clear:
            self.clear_text(element, visible=visible, timeout=timeout)

        ele = self.find_element(element, visible=visible, timeout=timeout)
        ele.send_keys(text)

        if press:
            # websites will get error, so silent it
            with suppress(Exception):
                ele.click()  # Focus on this element
            ele.send_keys(press)

    def get_text(self, element: tuple, /,
                 *, visible=True, timeout=TIMEOUT, show_log=False):
        try:
            ele = self.find_element(element, visible=visible, timeout=timeout, show_log=show_log)
            return ele.text
        except NoSuchElementException:
            return ""

    def is_displayed(self, element: tuple, /,
                     *, timeout=DISPLAY_TIMEOUT, show_log=False):
        try:
            return self.find_element(element, timeout=timeout, show_log=show_log).is_displayed()
        except NoSuchElementException:
            return ""

    def get_attribute(self, element: tuple, attribute="", /,
                      *, timeout=TIMEOUT, show_log=False):
        try:
            ele = self.find_element(element, timeout=timeout, show_log=show_log)
            return ele.get_attribute(attribute)
        except NoSuchElementException:
            return ""


class WebActions(Actions):

    def __init__(self, driver):
        super().__init__(driver)

    def click(
            self, element: tuple, /,
            *,
            timeout=TIMEOUT,
            show_log=True,
            visible=True,
    ):
        self.wait_for_element_clickable(element, timeout=timeout)
        ele = self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
        ele.click()

    def click_by_js(self, element: tuple, /, ):
        self._driver.execute_script("arguments[0].click();", self.find_element(element, visible=False))

    def scroll_to_view_by_js(self, x=0, y: str | int = "window.innerHeight"):
        self._driver.execute_script(f"window.scrollBy({x}, {y});")

    def hover(self, element: tuple, /, *, pause=2):
        self._action_chains.move_to_element(self.find_element(element)).pause(pause).perform()

    def double_click(self, element: tuple, /):
        self._action_chains.double_click(self.find_element(element)).perform()

    def right_click(self, element: tuple, /):
        self._action_chains.context_click(self.find_element(element)).perform()


class MobileActions(Actions):
    def __init__(self, driver):
        super().__init__(driver)
