from abc import ABCMeta, abstractmethod

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement


class DriverAware:

    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self, **kwargs):
        raise NotImplementedError

    @property
    def driver(self):
        raise NotImplementedError

    @abstractmethod
    def execute_script(self, script: str, element: WebElement, *args):
        raise NotImplementedError
