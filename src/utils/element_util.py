import functools
import logging
from contextlib import suppress

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as exc
from selenium.webdriver.support.wait import WebDriverWait

from src import consts
from src.consts import TIMEOUT, DISPLAY_TIMEOUT, MAX_RETRIES

_logger = logging.getLogger(consts.PYTHON_CONFIG)


class Actions:
    def __init__(self, driver):
        self._driver = driver
        self._action_chains = ActionChains(self._driver)

    def __wait_for_element__(self, element: tuple, /, *, func=None, timeout=TIMEOUT):
        webdriver_wait = WebDriverWait(self._driver, timeout, ignored_exceptions=(Exception,))
        return webdriver_wait.until(func(element))

    wait_for_element_visible = functools.partialmethod(__wait_for_element__, func=exc.visibility_of_element_located)
    wait_for_all_elements_visible = functools.partialmethod(
        __wait_for_element__, func=exc.visibility_of_all_elements_located)
    wait_for_element_not_visible = functools.partialmethod(
        __wait_for_element__, func=exc.invisibility_of_element_located)
    wait_for_element_presence = functools.partialmethod(__wait_for_element__, func=exc.presence_of_element_located)
    wait_for_all_elements_presence = functools.partialmethod(
        __wait_for_element__, func=exc.presence_of_all_elements_located)
    wait_for_element_clickable = functools.partialmethod(__wait_for_element__, func=exc.element_to_be_clickable)

    def wait_for_condition(self, condition_func, timeout=TIMEOUT, interval=0.1, *, show_log=False):
        """
        Wait until the given condition returns True using WebDriverWait.

        Args:
            condition_func: A lambda function that returns True when the desired condition is met
            timeout (float): Maximum time to wait in seconds
            interval (float): Time between condition checks in seconds

        Raises:
            TimeoutException: If the condition is not satisfied within the timeout period
        """
        try:
            WebDriverWait(self._driver, timeout, poll_frequency=interval).until(lambda d: condition_func())
        except TimeoutException:
            if show_log:
                _logger.error("Condition not met within timeout")

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

    def find_elements(
            self, element: tuple, /,
            *, timeout=TIMEOUT, visible=True, wait=True, show_log=True
    ) -> WebElement:
        with suppress(NoSuchElementException, TimeoutException):
            if wait:
                if visible:
                    return self.wait_for_all_elements_visible(element, timeout=timeout)
                return self.wait_for_all_elements_presence(element, timeout=timeout)
            return self._driver.find_elements(*element)

        msg_log = f"Element not found with locator {element[1]!r} after {timeout!r} seconds"
        if show_log:
            _logger.error(msg_log)
        raise NoSuchElementException(msg_log)

    def click(self, element: tuple, /, *, timeout=TIMEOUT, visible=True, show_log=True, retry=0):
        try:
            self.wait_for_element_clickable(element, timeout=timeout)
            ele = self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
            ele.click()
        except StaleElementReferenceException:
            if retry < MAX_RETRIES:
                self.click(element, timeout=timeout, visible=visible, show_log=show_log, retry=retry + 1)

    def clear_text(self, element: tuple, /, visible=False, timeout=TIMEOUT):
        self.find_element(element, visible=visible, timeout=timeout).clear()

    def send_keys(
            self, element: tuple, text, /,
            *, clear=True, press: Keys = "", visible=True, timeout=TIMEOUT, retry=0
    ):
        try:
            if clear:
                self.clear_text(element, visible=visible, timeout=timeout)

            ele = self.find_element(element, visible=visible, timeout=timeout)
            ele.send_keys(text)

            if press:
                # websites will get error, so silent it
                with suppress(Exception):
                    ele.click()  # Focus on this element
                ele.send_keys(press)
        except StaleElementReferenceException:
            if retry < MAX_RETRIES:
                self.send_keys(element, text, clear=clear, press=press, visible=visible, retry=retry + 1,
                               timeout=timeout)

    def get_text(self, element: tuple, /, *, visible=True, timeout=TIMEOUT, show_log=True):
        try:
            ele = self.find_element(element, visible=visible, timeout=timeout, show_log=show_log)
            return ele.text
        except NoSuchElementException:
            return ""

    def get_list_text(self, element: tuple, /, *, visible=True, timeout=TIMEOUT, show_log=True):
        try:
            list_ele = self.find_elements(element, visible=visible, timeout=timeout, show_log=show_log)
            return [ele.text for ele in list_ele]
        except NoSuchElementException:
            return []

    def is_displayed(self, element: tuple, /,
                     *, timeout=DISPLAY_TIMEOUT, show_log=True):
        try:
            return self.find_element(element, timeout=timeout, show_log=show_log).is_displayed()
        except NoSuchElementException:
            return ""

    def get_attribute(self, element: tuple, attribute="", /,
                      *, timeout=TIMEOUT, show_log=True, visible=True):
        try:
            ele = self.find_element(element, visible=visible, timeout=timeout, show_log=show_log)
            return ele.get_attribute(attribute)
        except NoSuchElementException:
            return ""


class WebActions(Actions):

    def __init__(self, driver):
        super().__init__(driver)

    # def click(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True, visible=True):
    #     with suppress(TimeoutException):
    #         self.wait_for_element_clickable(element, timeout=timeout)
    #         ele = self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
    #         ele.click()

    def click_by_js(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True):
        with suppress(TimeoutException):
            self._driver.execute_script(
                "arguments[0].click();",
                self.find_element(element, timeout=timeout, show_log=show_log, visible=False)
            )

    def scroll_to_view_by_js(self, x=0, y: str | int = "window.innerHeight"):
        self._driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_to_element(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True, visible=False, retry=0):
        with suppress(TimeoutException):
            self._driver.execute_script(
                "arguments[0].scrollIntoView();",
                self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
            )

    def hover(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True, visible=True, pause=2):
        with suppress(TimeoutException):
            self._action_chains.move_to_element(
                self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
            ).pause(pause).perform()

    def double_click(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True, visible=True):
        with suppress(TimeoutException):
            self._action_chains.double_click(
                self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
            ).perform()

    def right_click(self, element: tuple, /, *, timeout=TIMEOUT, show_log=True, visible=True):
        with suppress(TimeoutException):
            self._action_chains.context_click(
                self.find_element(element, timeout=timeout, show_log=show_log, visible=visible)
            ).perform()


class MobileActions(Actions):
    def __init__(self, driver):
        super().__init__(driver)
