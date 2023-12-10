import os
from time import sleep

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages_objects.account_registration_page import AccountRegistrationPage
from pages_objects.home_page import HomePage
from pages_objects.my_account_page import MyAccountPage
from utilities import XLUtils
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
    path = os.path.abspath(os.curdir) + "\\test_data\\Opencart_LoginData.xlsx"

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

    def test_register_user_with_empty_username_raises(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with empty username")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = ''
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_message = f"The Username field is required."
        message_element = self.register_page.get_error_message()
        message_element_text = message_element.text
        assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
        assert expected_message == message_element_text

    def test_register_user_with_username_les_then_5_chars(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with username less then 5 chars")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(3)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        expected_message = "The Username must be at least 5 characters long."
        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message_element_text
        except NoSuchElementException:
            raise AssertionError("The username can NOT be less then 5 characters")

    ############ Testing Registration Email Field ########################################

    def test_register_user_with_email_with_empty_email(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with empty email field")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = ''
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_message = "The Email field is required."

        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message_element_text
        except NoSuchElementException:
            raise AssertionError('Test Failed! Email can not be empty!')

    def test_register_user_with_email_without_at_symbol(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email without @ symbol")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = XLUtils.read_data(self.path, "Registration", 2, 1)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        expected_message = f"The Email field is not a valid e-mail address."
        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message_element_text
        except:
            raise AssertionError("The email must contain '@' symbol!")

    def test_register_user_with_email_without_domain(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email without domain")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = XLUtils.read_data(self.path, "Registration", 3, 1)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        expected_message = f"The Email field is not a valid e-mail address."
        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message_element_text
        except NoSuchElementException:
            raise AssertionError('Test Failed! Email must contains domain')

    @pytest.mark.regression
    def test_register_user_with_email_without_name(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email without name")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = '@yahoo.com'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_message = "The Email field is not a valid e-mail address."
        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert message_element_text == expected_message
        except NoSuchElementException:
            raise AssertionError('Test Failed! Email must contains name')
