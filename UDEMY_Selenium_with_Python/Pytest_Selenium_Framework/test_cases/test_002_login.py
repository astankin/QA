import os.path
from time import sleep

import pytest

from pages_objects.home_page import HomePage
from pages_objects.login_page import LoginPage
from pages_objects.my_account_page import MyAccountPage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestLogin:
    base_url = ReadConfig.get_application_url()
    logger = setup_logger(log_file_path='logs/register_account.log')

    username = ReadConfig.get_user()
    password = ReadConfig.get_password()

    @pytest.mark.sanity
    def test_login(self, setup):
        self.logger.info("**** Starting test_002_login ***")
        self.driver = setup
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        self.home_page = HomePage(self.driver)
        self.logger.info("click on [Login]")
        self.home_page.click_login()

        self.logger.info("Providing customer details for login")
        self.login_page = LoginPage(self.driver)
        self.login_page.set_username(self.username)
        self.login_page.set_password(self.password)
        self.login_page.click_login_btn()

        target_page = self.login_page.is_my_account_page_exists()
        self.my_account_page = MyAccountPage(self.driver).click_logout()
        if target_page:
            assert True
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False

        self.logger.info("**** End of the test_002_login ****")
