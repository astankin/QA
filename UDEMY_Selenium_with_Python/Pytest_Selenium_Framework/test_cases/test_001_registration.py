import os
from pages_objects.account_registration_page import AccountRegistrationPage
from pages_objects.home_page import HomePage
from utilities.read_properties import ReadConfig
from utilities.username_generator import generate_random_username


class TestAccountRegister:
    base_url = ReadConfig.get_application_url()

    def test_account_register(self, setup):
        self.driver = setup
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        self.home_page = HomePage(self.driver)
        self.home_page.click_register()

        self.register_page = AccountRegistrationPage(self.driver)
        self.username = generate_random_username(6)
        self.register_page.set_username(self.username)
        self.register_page.set_email(ReadConfig.get_email())
        self.register_page.set_password(ReadConfig.get_password())
        self.register_page.set_confirm_password(ReadConfig.get_password())
        self.register_page.set_first_name('John')
        self.register_page.set_last_name('Doe')
        self.register_page.click_register()
        self.confirm_msg = ""
        try:
            self.confirm_msg = self.register_page.get_confirm_msg()
        except:
            pass

        if self.confirm_msg == f"Welcome, {self.username}":
            assert True
            self.driver.close()
        else:
            screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
            screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
            self.driver.save_screenshot(screenshot_path)
            self.driver.close()
            assert False
