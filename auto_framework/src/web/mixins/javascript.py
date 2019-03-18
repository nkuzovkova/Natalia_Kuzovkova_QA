from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from auto_framework.src.general import Log
from auto_framework.src.web.support.web import DriverAware


class JSElementMixin:

    def __init__(self, driver: DriverAware, element: WebElement, element_name: str):
        self.driver = driver
        self.element = element
        self.element_name = element_name

    def execute(self, script, *args) -> str:
        return self.driver.execute_script(script, self.element, *args)

    def scroll_into_view(self):
        Log.info("Scrolling to '%s' element by JavaScript" % self.element_name)
        self.execute("arguments[0].scrollIntoView();")

    def click(self):
        Log.info("Clicking on '%s' element by JavaScript" % self.element_name)
        self.execute("arguments[0].click();")


class JSBrowserMixin:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)