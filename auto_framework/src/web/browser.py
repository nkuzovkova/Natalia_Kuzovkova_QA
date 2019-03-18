from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement

from auto_framework.src.web.mixins.javascript import JSBrowserMixin
from auto_framework.src.web.mixins.wait import WaitBrowserMixin
from auto_framework.src.web.drivers.drivers import Driver
from auto_framework.src.web.support.web import DriverAware
from ..general import Log


class Browser(DriverAware):

    __driver = None

    def find(self, **kwargs):
        pass

    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    @property
    def driver(self):
        return Browser.__driver

    @driver.setter
    def driver(self, driver):
        Browser.__driver = driver

    @property
    def wait_for(self) -> WaitBrowserMixin:
        return WaitBrowserMixin(self.driver)

    @property
    def js(self) -> JSBrowserMixin:
        return JSBrowserMixin(self.driver)

    def get(self, url: str, extensions: list=()):
        Log.info("Opening %s url" % url)
        if not self.driver:
            Log.info("Creating an instance of a Browser.")
            self.driver = Driver(extensions).create_session()
        self.driver.get(url)

    def refresh(self):
        Log.info("Refreshing the browser")
        self.driver.refresh()
        from selenium.common.exceptions import JavascriptException
        try:
            self.wait_for.page_is_loaded()
        except JavascriptException:
            pass

    def current_url(self):
        return self.driver.current_url

    def window_handles(self):
        return self.driver.window_handles

    def close(self):
        self.driver.close()

    def quit(self):
        if self.driver:
            Log.info("Closing the browser")
            try:
                self.driver.quit()
            except Exception as e:
                Log.error("Can't quit driver")
                Log.error(e)
            finally:
                self.driver = None