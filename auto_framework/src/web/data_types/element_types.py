import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from auto_framework.src.web.data_types import Locator
from auto_framework.src.web.data_types.auto_element_list import AutoElementList
from auto_framework.src.web.support.web import DriverAware
from ...general import Log
from ...web.data_types.actions import Action
from ...web.data_types.auto_element import AutoElement


class Input(AutoElement):
    """
      Prefix it with inp_
    """

    def __init__(self, page_object: DriverAware, locator: Locator, message_locator: Locator=None, **kwargs):
        AutoElement.__init__(self, page_object, locator, **kwargs)
        self.message_locator = message_locator

    def clear(self):
        Log.info("Clearing %s input field" % self.name)
        self.execute_action(Action.CLEAR)

    def send_keys(self, value: str):
        Log.info("Sending %s keys to the '%s' input field" % (value, self.name))
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def clear_and_send_keys(self, value: str):
        Log.info("Clearing and sending %s keys to the '%s' input field" % (value, self.name))
        self.clear()
        self.execute_action(Action.SEND_KEYS, expected_conditions.element_to_be_clickable, value)

    def get_message(self) -> str:
        return self.find().get_attribute("validationMessage")


class TextBlock(AutoElement):
    """
        Prefix it with txt_
    """


class Button(AutoElement):
    """
        Prefix it with btn_
    """


class AnyType(AutoElement):
    """
      Prefix it with ant_
    """
    pass


class SelectExtended(AutoElement):
    """
     Prefix it with slc_
    """

    def __init__(self, page_object: DriverAware, link_locator: Locator, option_list_locator: Locator=None,
                 message_locator: Locator=None, extent_list_by_click_on_field: bool=True,
                 hide_list_by_click_on_field: bool=False, **kwargs):
        AutoElement.__init__(self, page_object, link_locator, **kwargs)
        self.extent_list_by_click_on_field = extent_list_by_click_on_field
        self.hide_list_by_click_on_field = hide_list_by_click_on_field
        if option_list_locator:
            self.options_list = AutoElementList(page_object, option_list_locator)
        if message_locator:
            self.message = TextBlock(page_object, message_locator)

    def select_item_by_value(self, value: str):
        Log.info('Selecting %s value in the %s select list' % (value, self.name))
        Select(self.wait_for.presence_of_element_located()).select_by_value(value)

    def select_item_by_visible_text(self, value: str):
        Log.info('Selecting %s text in the %s select list' % (value, self.name))
        Select(self.wait_for.presence_of_element_located()).select_by_visible_text(value)

    def first_selected_option(self):
        Log.info('Get first selected option in the %s select list' % self.name)
        return Select(self.wait_for.presence_of_element_located()).first_selected_option

    def select_item_by_text(self, text: str, delay_for_options_to_appear_time: int=0.5):
        Log.info("Selecting %s in the '%s' select list" % (text, self.name))
        if self.extent_list_by_click_on_field:
            self.execute_action(Action.CLICK)
            time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.wait_for.presence_of_all_elements_located()
        for option in options:
            if option.text == text:
                option.click()
                break
        if self.hide_list_by_click_on_field:
            self.execute_action(Action.CLICK)

    def get_options_list(self, delay_for_options_to_appear_time: int=0.5):
        Log.info("Getting all options list from the '%s' select list" % self.name)
        out = list()
        self.execute_action(Action.CLICK)
        time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.wait_for.presence_of_all_elements_located()
        for option in options:
            out.append(option.text)
        return out

    def select_option_by_attribute_value(self, attribute_name: str, attribute_value: str,
                                         delay_for_options_to_appear_time: int=0.5):
        Log.info("Selecting option by attribute '%s' with value '%s' in the '%s' select list"
                 % (attribute_name, attribute_value, self.name))
        self.execute_action(Action.CLICK)
        time.sleep(delay_for_options_to_appear_time)
        options = self.options_list.wait_for.presence_of_all_elements_located()
        for option in options:
            if option.get_attribute(attribute_name) == attribute_value:
                option.click()
                break

    def get_message(self) -> str:
        return self.message.text