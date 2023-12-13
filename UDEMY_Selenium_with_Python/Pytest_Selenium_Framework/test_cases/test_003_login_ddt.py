import time

import os

import pytest

from pages_objects.home_page import HomePage
from pages_objects.login_page import LoginPage
from pages_objects.my_account_page import MyAccountPage
from utilities import XLUtils
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestLoginDDT:
    baseURL = ReadConfig.get_application_url()
    logger = setup_logger(log_file_path='logs/register_account.log')

    path = os.path.abspath(os.curdir) + "\\test_data\\Opencart_LoginData.xlsx"

    def test_login_ddt(self, setup):
        self.logger.info("**** Starting test_003_login_Datadriven *******")
        self.rows = XLUtils.getRowCount(self.path, 'Sheet1')
        lst_status = []

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.my_account_page = MyAccountPage(self.driver)

        for r in range(2, self.rows + 1):
            self.home_page.click_login()

            self.username = XLUtils.read_data(self.path, "Sheet1", r, 1)
            self.password = XLUtils.read_data(self.path, "Sheet1", r, 2)
            self.expected = XLUtils.read_data(self.path, "Sheet1", r, 3)

            self.login_page.set_username(self.username)
            self.login_page.set_password(self.password)
            self.login_page.click_login_btn()

            time.sleep(3)
            self.target_page = self.login_page.is_my_account_page_exists()

            if self.expected == 'Valid':
                if self.target_page:
                    lst_status.append('Pass')
                    self.my_account_page.click_logout()
                else:
                    lst_status.append('Fail')
            elif self.expected == 'Invalid':
                if self.target_page:
                    lst_status.append('Fail')
                    self.my_account_page.click_logout()
                else:
                    lst_status.append('Pass')

        if "Fail" not in lst_status:
            assert True
        else:
            assert False
        self.logger.info("******* End of test_003_login_Datadriven **********")
