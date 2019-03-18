from abc import ABCMeta

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from auto_framework.src.web.data_types.base_element import BaseElement
from auto_framework.src.web.mixins.wait import WaitElementsMixin
from ...general import Log


class AutoElementList(BaseElement):

    __metaclass__ = ABCMeta

    def find(self, wait_time: int=0):
        return self.wait_for.presence_of_all_elements_located(wait_time)

    @property
    def wait_for(self) -> WaitElementsMixin:
        return WaitElementsMixin(self.driver, self.locator)

    def exists(self, wait_time: int=0):
        Log.info("Checking if '%s' list of elements exists" % self.name)
        try:
            self.wait_for.presence_of_all_elements_located(wait_time)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    @property
    def size(self):
        return len(self.wait_for.presence_of_all_elements_located())

    @property
    def elements_texts(self):
        return [element.text for element in self.wait_for.presence_of_all_elements_located()]

    def select_first_enabled(self):
        Log.info("Selecting first enabled item in the list '%s'" % self.name)
        elements = self.wait_for.presence_of_all_elements_located()
        for item in elements:
            if item.is_enabled():
                item.click()
                break