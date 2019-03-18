from auto_framework.src.web import http_request_wait_time
from auto_framework.src.web.data_types import CssSelector, Xpath
from auto_framework.src.web.data_types.element_types import Input, Button, SelectExtended, TextBlock
from auto_framework.src.web.page_object import PageObject
from auto_framework.src.web.support.page_factory import find_by
from src import login_url
from src.const import LANG_CODE


@find_by(Xpath("//p[@ng-show='!newUser'][not(contains(@class, 'ng-hide'))]/.."))
class LoginPage(PageObject):

    def __init__(self):
        # Page elements
        self.inp_user_name = Input(self, CssSelector("#username"))
        self.inp_password = Input(self, CssSelector("#password"))
        self.btn_sign_in = Button(self, CssSelector("button"))
        self.ddl_language = SelectExtended(self, CssSelector(".lang_selected"), CssSelector(".lang_name"), hide_list_by_click_on_field=True)
        self.txt_lang_code = TextBlock(self, CssSelector(".lang_code"))
        self.txt_error = TextBlock(self, Xpath("//span[@class='warning']"))
        self.btn_forgot_password = Button(self, Xpath("//a[contains(@ng-bind, 'FORGOT PASSWORD')]"))
        self.btn_create_new_account = Button(self, Xpath("//span[contains(@ng-bind, 'CREATE NEW ACCOUNT')]"))

    def open_actions(self):
        self.get(login_url)

    def login(self, user_name_value, password_value):
        if user_name_value:
            self.inp_user_name.clear_and_send_keys(user_name_value)
        if password_value:
            self.inp_password.clear_and_send_keys(password_value)
        self.btn_sign_in.js.click()
        return self

    def change_lang(self, lang):
        self.ddl_language.select_item_by_text(LANG_CODE[lang])
        self.txt_lang_code.wait_for.text_to_be_present_in_element(lang, wait_time=http_request_wait_time)
        return self

    def get_error_text(self):
        try:
            self.txt_error.wait_for.text_equal("", wait_time=5, until=False)
        except TimeoutError:
            pass
        return self.txt_error.text

