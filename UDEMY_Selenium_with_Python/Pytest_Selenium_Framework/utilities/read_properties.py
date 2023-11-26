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


