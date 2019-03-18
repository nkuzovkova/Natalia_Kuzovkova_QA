from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from ...web.drivers import capabilities


class Driver:

    def __init__(self, extensions=None):
        self.extensions = extensions

    @staticmethod
    def get_driver_type(browser_name):
        if browser_name == 'chrome':
            return Chrome

    def get_local_session(self):
        driver_type = self.get_driver_type(capabilities['browserName'])
        driver_capabilities = {**driver_type.get_capabilities(self.extensions), **capabilities}
        return driver_type.get_session(driver_capabilities)

    def create_session(self):
        driver = self.get_local_session()
        width = int(capabilities['browserSize'].split('x')[0])
        height = int(capabilities['browserSize'].split('x')[1])
        driver.set_window_size(width, height)
        driver.set_window_position(0, 0)
        return driver


class Chrome(Driver):

    @classmethod
    def get_capabilities(cls, extensions=None):
        from selenium.webdriver.chrome.webdriver import Options as ChromeOptions
        chrome_options = ChromeOptions()
        if extensions:
            for extension in extensions:
                chrome_options.add_extension(extension)
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        chrome_capabilities = chrome_options.to_capabilities()
        chrome_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        return chrome_capabilities

    @classmethod
    def get_session(cls, driver_capabilities):
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=driver_capabilities)
        return driver