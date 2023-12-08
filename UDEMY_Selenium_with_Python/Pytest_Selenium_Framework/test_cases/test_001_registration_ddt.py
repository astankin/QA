import os
from time import sleep

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages_objects.account_registration_page import AccountRegistrationPage
from pages_objects.home_page import HomePage
from pages_objects.my_account_page import MyAccountPage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig
from utilities.username_generator import generate_random_username


class TestUserRegistration:
    username = generate_random_username(7)
    email = ReadConfig.get_email()
    password = ReadConfig.get_password()
    conf_password = ReadConfig.get_password()
    first_name = ReadConfig.get_first_name()
    last_name = ReadConfig.get_last_name()
    base_url = ReadConfig.get_application_url()
    chars = ReadConfig.get_chars_list()
    logger = setup_logger(log_file_path='logs/register_account.log')

    def open_register_form(self, setup):
        self.driver = setup
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        self.home_page = HomePage(self.driver)
        self.logger.info("click on [Register]")
        self.home_page.click_register()

    @pytest.mark.sanity
    def test_registration_with_valid_data(self, setup):
        self.logger.info("*** test_001_AccountRegistration started ***")
        self.open_register_form(setup)

        self.logger.info("Providing customer details for registration")
        self.register_page = AccountRegistrationPage(self.driver)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
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

    def test_register_with_existing_username(self, setup):
        username = 'astankin235'
        self.open_register_form(setup)

        self.register_page = AccountRegistrationPage(self.driver)
        self.register_page.register(
            username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        expected_message = f"Username '{username}' is already taken."
        error_message = self.register_page.get_error_message()
        assert error_message.is_displayed()
        assert expected_message == error_message.text

    def test_register_with_username_contains_white_space(self, setup):
        self.open_register_form(setup)

        self.logger.info("Providing customer details for registration")
        self.register_page = AccountRegistrationPage(self.driver)
        usernames = [' username', 'username ', 'user name']
        status_list = []
        for username in usernames:
            self.logger.info(f"Entered {username}")

            self.register_page.register(
                username,
                self.email,
                self.password,
                self.conf_password,
                self.first_name,
                self.last_name
            )
            sleep(3)
            self.expected_message = f"Username '{username}' is invalid, can only contain letters or digits."
            try:
                message_text = self.register_page.get_error_message()
                if message_text.is_displayed() and self.expected_message == message_text.text:
                    status_list.append('Passed')
                else:
                    status_list.append('Fail')
            except NoSuchElementException:
                self.logger.info("Registration FAILED")
                status_list.append('Fail')
                self.my_account_page = MyAccountPage(self.driver)
                self.my_account_page.click_logout()

            self.register_page.click_register_link()

        if 'Fail' not in status_list:
            self.logger.info("Registration PASSED")
            assert True
        else:
            self.logger.info("Registration FAILED")
            assert False

        self.logger.info("******* End of test_001_register_Datadriven **********")

    @pytest.mark.regression
    def test_register_user_with_username_contains_special_char(self, setup):
        self.open_register_form(setup)
        self.logger.info("Providing customer details for registration")
        self.register_page = AccountRegistrationPage(self.driver)
        usernames_with_char = [self.username + str(char) for char in self.chars]
        not_allowed_chars = []
        for username in usernames_with_char:
            self.register_page.register(
                username,
                self.email,
                self.password,
                self.conf_password,
                self.first_name,
                self.last_name
            )

            expected_message = f"Username '{username}' is invalid, can only contain letters or digits."
            try:
                message_element = self.register_page.get_error_message()
                assert message_element.is_displayed()
                assert expected_message == message_element.text
            except NoSuchElementException:
                not_allowed_chars.append(username[-1])
                self.my_account_page = MyAccountPage(self.driver)
                self.my_account_page.click_logout()
            self.home_page = HomePage(self.driver)
            self.home_page.click_register()
        if len(not_allowed_chars) > 0:
            raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")
