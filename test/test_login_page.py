import pytest

from src.const import ERROR_MESSAGE, DEFAULT_LANG
from src.user_entity.user_entity import UserFactory, User
from src.login_page import LoginPage


class TestLogin:

    @pytest.fixture(scope="function")
    def fx_fn_login_page(self, request):
        def finalizer():
            LoginPage().quit()
        request.addfinalizer(finalizer)
        return LoginPage().open()

    test_login_invalid_credentials_data = [pytest.param(UserFactory.empty_user_name_password(), ERROR_MESSAGE[DEFAULT_LANG]),
                                           pytest.param(UserFactory.empty_password(), ERROR_MESSAGE[DEFAULT_LANG]),
                                           pytest.param(UserFactory.empty_user_name(), ERROR_MESSAGE[DEFAULT_LANG]),
                                           pytest.param(UserFactory.wrong_user_name(), ERROR_MESSAGE[DEFAULT_LANG]),
                                           pytest.param(UserFactory.wrong_password(), ERROR_MESSAGE[DEFAULT_LANG]),
                                           pytest.param(UserFactory.wrong_user_name_password(), ERROR_MESSAGE[DEFAULT_LANG])
                                          ]

    @pytest.mark.parametrize("user, expected_error", test_login_invalid_credentials_data)
    def test_login_invalid_credentials(self, fx_fn_login_page, user: User, expected_error):
        """Validate different combination of user credentials"""
        actual_error = fx_fn_login_page.change_lang(DEFAULT_LANG).login(user.user_name, user.password).get_error_text()
        assert actual_error == expected_error,\
            "Actual error message '%s' is equal to expected '%s'" %\
            (actual_error, expected_error)

    @pytest.mark.parametrize("lang", ["EN", "FR", "PT", "ES", "RU", "JA"])
    def test_login_error_message_localization(self, fx_fn_login_page, lang):
        """Validate error message for different languages """
        fx_fn_login_page.change_lang(lang)
        fx_fn_login_page.login(None, None)
        actual_error = fx_fn_login_page.get_error_text()
        assert actual_error == ERROR_MESSAGE[lang],\
            "For %s language actual error message '%s' is equal to expected '%s'" %\
            (lang, actual_error, ERROR_MESSAGE[lang])

    #It can be extended with more cases
    test_login_invalid_data = [pytest.param(None, "Please fill out this field."),
                               pytest.param("a", "Please include an '@' in the email address. 'a' is missing an '@'."),
                               pytest.param("@", "Please enter a part followed by '@'. '@' is incomplete."),
                               pytest.param("@a", "Please enter a part followed by '@'. '@a' is incomplete."),
                               pytest.param("a@", "Please enter a part following '@'. 'a@' is incomplete."),
                               pytest.param("a@@", "A part following '@' should not contain the symbol '@'."), # any special characters
                               pytest.param("a@.", "'.' is used at a wrong position in '.'."),
                               pytest.param("a@a.", "'.' is used at a wrong position in 'a.'.")
                               ]

    @pytest.mark.parametrize("user_name, validation_message", test_login_invalid_data)
    def test_login_user_name_validation(self, fx_fn_login_page, user_name, validation_message):
        """Validate user name fild validation message"""
        fx_fn_login_page.login(user_name, None)
        actual_message = fx_fn_login_page.inp_user_name.get_message()
        assert actual_message == validation_message, \
            "Actual validatin message '%s' is not equal to expected '%s'" % (actual_message, validation_message)

    #Test cases for password validation can be added