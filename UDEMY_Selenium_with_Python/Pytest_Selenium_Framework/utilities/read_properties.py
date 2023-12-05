import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '\\configurations\\config.ini')


class ReadConfig:
    @staticmethod
    def get_application_url():
        url = config.get('commonInfo', 'base_url')
        return url

    @staticmethod
    def get_password():
        password = config.get('commonInfo', 'password')
        return password

    @staticmethod
    def get_email():
        email = config.get('commonInfo', 'email')
        return email

    @staticmethod
    def get_user():
        user_name = config.get('commonInfo', 'user_name')
        return user_name

    @staticmethod
    def get_first_name():
        first_name = config.get('commonInfo', 'first_name')
        return first_name

    @staticmethod
    def get_last_name():
        last_name = config.get('commonInfo', 'last_name')
        return last_name

    @staticmethod
    def get_chars_list():
        chars = config.get('commonInfo', 'chars').split(', ')
        return chars



