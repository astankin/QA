import os

import pytest

from pages_objects.account_registration_page import AccountRegistrationPage
from pages_objects.home_page import HomePage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig
from utilities.username_generator import generate_random_username


class TestAccountRegister:
    base_url = ReadConfig.get_application_url()
    logger = setup_logger(log_file_path='logs/register_account.log')

    @pytest.mark.sanity
    def test_account_register(self, setup):
        self.logger.info("*** test_001_AccountRegistration started ***")
        self.driver = setup
        self.driver.get(self.base_url)
        self.logger.info("Launching application")
        self.driver.maximize_window()

        self.home_page = HomePage(self.driver)
        self.logger.info("click on [Register]")
        self.home_page.click_register()

        self.logger.info("Providing customer details for registration")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(6)
        self.register_page.set_username(self.username)
        self.register_page.set_email(ReadConfig.get_email())
        self.register_page.set_password(ReadConfig.get_password())
        self.register_page.set_confirm_password(ReadConfig.get_password())
        self.register_page.set_first_name(ReadConfig.get_first_name())
        self.register_page.set_last_name(ReadConfig.get_last_name())
        self.register_page.click_register()
        self.confirm_msg = ""
        try:
            self.confirm_msg = self.register_page.get_confirm_msg()
        except:
            pass

        if self.confirm_msg == f"Welcome, {self.username}":
            self.logger.info("Registration PASSED")
            assert True
            self.driver.close()
        else:
            screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
            screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
            self.driver.save_screenshot(screenshot_path)
            self.logger.info("Registration FAILED")
            self.driver.close()
            assert False
        self.logger.info("*** test_001_AccountRegistration finished ***")
