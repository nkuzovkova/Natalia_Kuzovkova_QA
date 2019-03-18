from collections import Iterable

from selenium.webdriver.common.by import By


class Locator(Iterable):

    def __iter__(self):
        yield self.by
        yield self.value

    def __init__(self, by, value):
        self.by = by
        self.value = value

    def __repr__(self):
        return "%s: %s" % (self.by, self.value)


class Xpath(Locator):

    def __init__(self, value):
        super().__init__(By.XPATH, value)


class CssSelector(Locator):

    def __init__(self, value):
        super().__init__(By.CSS_SELECTOR, value)
