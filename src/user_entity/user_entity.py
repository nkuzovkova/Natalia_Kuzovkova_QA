from src.user_entity import default_password, default_user
from auto_framework.src.general import Random


class User:
    """Storage of all user properties.
    In the future can be extended with email, permissions, etc.
    """
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password


class UserFactory:

    @staticmethod
    def wrong_user_name():
        return User(Random.rand_string(10), default_password)

    @staticmethod
    def wrong_password():
        return User(default_user, Random.rand_string(10))

    @staticmethod
    def wrong_user_name_password():
        return User(Random.rand_string(10), Random.rand_string(10))

    @staticmethod
    def empty_user_name():
        return User(None, default_password)

    @staticmethod
    def empty_password():
        return User(default_user, None)

    @staticmethod
    def empty_user_name_password():
        return User(None, None)