import os
import random
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

    def test_register_form_submit_with_empty_fields_error_messages_are_displayed(self, setup):
        self.logger.info("Starting register with empty fields")
        self.open_register_form(setup)
        self.register_page = AccountRegistrationPage(self.driver)
        self.register_page.click_register()
        error_messages = self.driver.find_elements(By.CSS_SELECTOR, "div.text-danger.validation-summary-errors ul li")
        messages = []
        for message in error_messages:
            messages.append(message.text)
        assert "The Username field is required." in messages
        assert "The Email field is required." in messages
        assert "The Password field is required." in messages
        assert "The First Name field is required." in messages
        assert "The Last Name field is required." in messages

    def test_register_with_existing_username(self, setup):

        self.username = 'username'
        self.open_register_form(setup)

        self.register_page = AccountRegistrationPage(self.driver)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        expected_message = f"Username '{self.username}' is already taken."
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

    def test_register_user_with_empty_username_field(self, setup):
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

    def test_register_user_with_numbers_only(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test username contains only numbers")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = random.randint(100000, 999999)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_message = f"The Username field is required."
        try:
            message_element = self.register_page.get_error_message()
            message_element_text = message_element.text
            assert message_element.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message_element_text
        except:
            raise AssertionError("The username can NOT contains numbers")

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
        self.username = generate_random_username(7)
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
        self.username = generate_random_username(9)
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
        self.username = generate_random_username(5)
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

    def test_register_user_with_email_without_name(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email without name")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = '@yahoo.com'
        self.username = generate_random_username(5)
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

    def test_register_user_with_email_with_more_then_one_domain_name(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email with more domains")
        self.register_page = AccountRegistrationPage(self.driver)
        self.email = XLUtils.read_data(self.path, "Registration", 4, 1)
        self.username = generate_random_username(5)
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_message = f"Welcome, {self.username}"
        try:
            message_element = self.register_page.get_confirm_msg()
            assert expected_message == message_element
            expected_url = "http://softuni-qa-loadbalancer-2137572849.eu-north-1.elb.amazonaws.com:81/"
            assert expected_url == self.driver.current_url
        except:
            assert False

    def test_register_user_with_email_contains_special_char(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with email contains special char")
        self.register_page = AccountRegistrationPage(self.driver)
        not_allowed_chars = []
        base_email = 'something'
        domain = '@yahoo.com'
        emails = [base_email + char for char in self.chars]
        for email in emails:
            self.username = generate_random_username(5)
            char = email[-1]
            email += domain
            self.register_page.register(
                self.username,
                email,
                self.password,
                self.conf_password,
                self.first_name,
                self.last_name
            )
            expected_message = 'The Email field is not a valid e-mail address.'
            try:
                message_element = self.register_page.get_error_message()
                message_element_text = message_element.text
                assert expected_message == message_element_text
            except NoSuchElementException:
                not_allowed_chars.append(char)
                self.my_account_page = MyAccountPage(self.driver)
                self.my_account_page.click_logout()
            self.home_page = HomePage(self.driver)
            self.home_page.click_register()
        if not_allowed_chars:
            raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")

    #################### Testing Password Field ########################################################

    def test_register_user_with_password_less_then_5_symbols(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with password les then 5 symbols")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(7)
        self.password1 = 'pass'
        self.password2 = 'pass'
        self.register_page.register(
            self.username,
            self.email,
            self.password1,
            self.password2,
            self.first_name,
            self.last_name
        )
        expected_error_text = "The Password must be at least 6 and at max 20 characters long."
        try:
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The Password must be at least 6 characters long")

    def test_register_user_with_empty_password(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with empty password field")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(8)
        self.password = ""
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_error_text = "The Password field is required."
        try:
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except NoSuchElementException:
            raise AssertionError("The password can not be an empty string!")

    def test_register_user_with_empty_confirm_password(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with empty confirm password field")
        self.register_page = AccountRegistrationPage(self.driver)
        username = generate_random_username(7)
        self.conf_password = ""
        self.register_page.register(
            username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_error_text = "The password2 must match password1."
        try:
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed(), "Error message is not displayed"
            assert error_text.text == expected_error_text, "Unexpected error message"
        except NoSuchElementException:
            raise AssertionError("The confirm password field can NOT be empty")
        self.logger.info("Finished test with empty confirm password field")

    @pytest.mark.regression
    def test_register_user_with_confirm_password_mismatch_password(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with confirm password mismatch password")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(7)
        self.conf_password = "wrong"
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        expected_error_text = "The password2 must match password1"
        try:
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except NoSuchElementException:
            raise AssertionError("The confirm password must be the same as password")

    ################ Testing First Name Field ################################################

    def test_register_user_with_first_name_length_les_then_2_letters(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with confirm first name less then 2 letters")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(8)
        self.first_name = 'J'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The name must be at least 2 letters long."
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The first name must be at least 2 letters long.")

    def test_register_user_with_first_name_empty_string(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with confirm first name empty field")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(8)
        self.first_name = ''
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The First Name field is required."
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The first name must be at least 2 letters long.")

    def test_register_user_with_first_name_contains_only_numbers(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with first name contains only numbers")
        self.register_page = AccountRegistrationPage(setup)
        self.username = generate_random_username(9)
        self.first_name = '123456'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        try:
            expected_error_text = "The name must contains only letters"
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The first name must contains only letters")

    def test_register_user_with_first_name_contains_special_characters(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with first name contains special char")
        self.register_page = AccountRegistrationPage(setup)
        f_name_with_char = [self.username + str(char) for char in self.chars]
        not_allowed_chars = []
        for f_name in f_name_with_char:
            self.username = generate_random_username(7)
            self.register_page.register(
                self.username,
                self.email,
                self.password,
                self.conf_password,
                f_name,
                self.last_name
            )

            try:
                expected_error_text = "The name must contains only letters"
                error_text = self.register_page.get_error_message()
                assert error_text.is_displayed()
                assert error_text.text == expected_error_text
            except NoSuchElementException:
                not_allowed_chars.append(f_name[-1])
                self.my_account_page = MyAccountPage(self.driver)
                self.my_account_page.click_logout()
            self.home_page = HomePage(self.driver)
            self.home_page.click_register()

        if len(not_allowed_chars) > 0:
            raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")

    def test_register_user_with_first_name_contains_white_space(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with first name contains white space")
        self.register_page = AccountRegistrationPage(setup)
        self.username = generate_random_username(6)
        self.first_name = 'John Doe'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The name must contains only letters"
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("First name can not contains white space")

    ################ Testing Last Name Field ##################################################

    @pytest.mark.current
    def test_register_user_with_last_name_length_les_then_2_letters(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with confirm last name less then 2 letters")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(8)
        self.last_name = 'D'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The name must be at least 2 letters long."
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The last name must be at least 2 letters long.")

    def test_register_user_with_last_name_empty_string(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with last name empty field")
        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(8)
        self.last_name = ''
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The First Name field is required."
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The last name must be at least 2 letters long.")

    def test_register_user_with_last_name_contains_only_numbers(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with last name contains only numbers")
        self.register_page = AccountRegistrationPage(setup)
        self.username = generate_random_username(9)
        self.last_name = '123456'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )
        try:
            expected_error_text = "The name must contains only letters"
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("The last name must contains only letters")

    def test_register_user_with_last_name_contains_special_characters(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with last name contains special char")
        self.register_page = AccountRegistrationPage(setup)
        l_name_with_char = [self.username + str(char) for char in self.chars]
        not_allowed_chars = []
        for l_name in l_name_with_char:
            self.username = generate_random_username(7)
            self.register_page.register(
                self.username,
                self.email,
                self.password,
                self.conf_password,
                self.first_name,
                l_name
            )
            try:
                expected_error_text = "The name must contains only letters"
                error_text = self.register_page.get_error_message()
                assert error_text.is_displayed()
                assert error_text.text == expected_error_text
            except NoSuchElementException:
                not_allowed_chars.append(l_name[-1])
                self.my_account_page = MyAccountPage(self.driver)
                self.my_account_page.click_logout()
            self.home_page = HomePage(self.driver)
            self.home_page.click_register()

        if len(not_allowed_chars) > 0:
            raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")

    def test_register_user_with_last_name_contains_white_space(self, setup):
        self.open_register_form(setup)
        self.logger.info("Starting test with first name contains white space")
        self.register_page = AccountRegistrationPage(setup)
        self.username = generate_random_username(9)
        self.last_name = 'John Doe'
        self.register_page.register(
            self.username,
            self.email,
            self.password,
            self.conf_password,
            self.first_name,
            self.last_name
        )

        try:
            expected_error_text = "The name must contains only letters"
            error_text = self.register_page.get_error_message()
            assert error_text.is_displayed()
            assert error_text.text == expected_error_text
        except:
            raise AssertionError("Last name can NOT contains white space!")
