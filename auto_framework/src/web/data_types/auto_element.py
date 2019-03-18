import time
from abc import ABCMeta

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    WebDriverException, InvalidElementStateException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

from auto_framework.src.general import Log
from auto_framework.src.web import retry_delay
from auto_framework.src.web.data_types.actions import Action
from auto_framework.src.web.data_types.base_element import BaseElement
from auto_framework.src.web.mixins.javascript import JSElementMixin
from auto_framework.src.web.mixins.wait import WaitElementMixin


class AutoElement(BaseElement):

    __metaclass__ = ABCMeta

    def find(self, wait_time: int=0, **kwargs):
        return self.wait_for.presence_of_element_located(wait_time)

    @property
    def wait_for(self) -> WaitElementMixin:
        return WaitElementMixin(self.driver, self.locator)

    @property
    def js(self) -> JSElementMixin:
        return JSElementMixin(self.ancestor, self.wait_for.presence_of_element_located(), self.name)

    def exists(self, wait_time: int=0) -> bool:
        Log.info("Checking if '%s' element exists" % self.name)
        try:
            self.wait_for.presence_of_element_located(wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def execute_action(self, action, element_condition: expected_conditions=presence_of_element_located, *args):
        try:
            obj = getattr(self.wait_for.condition(wait_time=1, condition=element_condition(self.locator)), action)
            if isinstance(obj, str):
                self._retry_count = 0
                return obj
            else:
                if args:
                    value = obj(*args)
                else:
                    value = obj()
                return value
        except (StaleElementReferenceException, WebDriverException, InvalidElementStateException) as e:
            if self._retry_count <= 2:
                self._retry_count += 1
                Log.error('Error on performing \'%s\' action. Retrying...' % action)
                Log.error(e.msg)
                time.sleep(retry_delay)
                if 'is not clickable at point' in e.msg:
                    self.js.scroll_into_view()
                return self.execute_action(action, element_condition, *args)
            else:
                raise e

    @property
    def type(self):
        return self.__class__.__name__

    # Native WebElement methods
    def click(self, element_condition: expected_conditions=element_to_be_clickable):
        Log.info('Clicking on the "%s" "%s"' % (self.name, self.type))
        self.execute_action(Action.CLICK, element_condition)

    def get_attribute(self, name: str):
        Log.info('Getting attribute value from "%s" "%s"' % (self.name, self.type))
        return self.execute_action(Action.GET_ATTRIBUTE, presence_of_element_located, name)

    @property
    def text(self) -> str:
        Log.info('Getting text from "%s" "%s"' % (self.name, self.type))
        result = self.execute_action(Action.TEXT)
        Log.info('Actual text from "%s" "%s" is "%s"' % (self.name, self.type, result))
        return result

