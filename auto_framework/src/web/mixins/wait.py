from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait, POLL_FREQUENCY

from auto_framework.src.general import Log
from auto_framework.src.web import element_load_time, page_load_time
from auto_framework.src.web.data_types import Locator
from auto_framework.src.web.support.web import DriverAware


class text_equal(object):
    """ An expectation for checking if specified element text equal expected text value.
    locator, text
    """

    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = driver.find_element(*self.locator).text
            return self.text == element_text
        except StaleElementReferenceException:
            return False


class text_not_equal(object):
    """ An expectation for checking if specified element text does not equal expected text value.
    locator, text
    """

    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = driver.find_element(*self.locator).text
            return self.text != element_text
        except StaleElementReferenceException:
            return False


class attribute_value_in_element(object):
    """ An expectation for checking if the given attribute value is present in the  specified element.
    locator, text
    """

    def __init__(self, locator, attribute_, value_):
        self.locator = locator
        self.attribute = attribute_
        self.value = value_

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            return self.value in element.get_attribute(self.attribute)
        except StaleElementReferenceException:
            return False


class WaitMixin:

    def __init__(self, driver: DriverAware):
        self.driver = driver

    def condition(self, wait_time: int, condition: expected_conditions, poll_frequency: float = POLL_FREQUENCY,
                  ignored_exceptions: list = None, until=True):
        if until:
            return WebDriverWait(self.driver, wait_time, poll_frequency, ignored_exceptions).until(condition)
        else:
            return not WebDriverWait(self.driver, wait_time, poll_frequency, ignored_exceptions).until_not(condition)


class WaitElementMixin(WaitMixin):

    def __init__(self, driver: DriverAware, element_locator: Locator):
        super().__init__(driver)
        self.locator = element_locator
        self.name = str(self.locator)

    def presence_of_element_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                    ignored_exceptions=None):
        Log.info('An expectation for checking that an element "%s" is present on the DOM of a page.' % self.name)
        return self.condition(wait_time, presence_of_element_located(self.locator), poll_frequency, ignored_exceptions)

    def text_to_be_present_in_element(self, text: str, wait_time: int = element_load_time,
                                      poll_frequency=POLL_FREQUENCY,
                                      ignored_exceptions=None, until=True):
        Log.info('Checking if the given text is present in the specified element "%s".' % self.name)
        return self.condition(wait_time, text_to_be_present_in_element(self.locator, text), poll_frequency,
                              ignored_exceptions, until)

    def text_equal(self, text: str, wait_time: int = element_load_time,
                   poll_frequency=POLL_FREQUENCY, ignored_exceptions=None, until=True):
        Log.info('Checking if the given text equal the element\'s locator "%s", text.' % self.name)
        return self.condition(wait_time, text_equal(self.locator, text), poll_frequency, ignored_exceptions, until)


class WaitElementsMixin(WaitMixin):

    def __init__(self, driver: DriverAware, element_locator: Locator):
        super().__init__(driver)
        self.locator = element_locator
        self.name = str(self.locator)

    def presence_of_all_elements_located(self, wait_time: int = element_load_time, poll_frequency=POLL_FREQUENCY,
                                         ignored_exceptions=None):
        Log.info('An expectation for checking that there is at least one element "%s" present on a web page.'
                 % self.name)
        return self.condition(wait_time, presence_of_all_elements_located(self.locator), poll_frequency,
                              ignored_exceptions)


class WaitBrowserMixin(WaitMixin):

    def __init__(self, driver: DriverAware):
        super().__init__(driver)

    def page_is_loaded(self, wait_time: int = page_load_time, poll_frequency=POLL_FREQUENCY,
                       ignored_exceptions=None):
        Log.info('Waiting for page to be loaded.')
        self.condition(wait_time, lambda driver: driver.execute_script('return document.readyState') == 'complete',
                       poll_frequency, ignored_exceptions)
        Log.info("Waiting for page to be loaded: Success")
