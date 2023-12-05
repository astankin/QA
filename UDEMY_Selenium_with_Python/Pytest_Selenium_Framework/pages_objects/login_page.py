from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    input_username_id = "Input_Username"
    input_password_id = "Input_Password"
    btn_login_xpath = "//*[@id='account']/div[4]/button"
    register_as_new_user_text = "Register as a new user"
    welcome_msg_xpath = "/html/body/div/main/div/h1"

    def __init__(self, driver):
        self.driver = driver

    def set_username(self, username):
        self.driver.find_element(By.ID, self.input_username_id).send_keys(username)

    def set_password(self, password):
        self.driver.find_element(By.ID, self.input_password_id).send_keys(password)

    def click_login_btn(self):
        self.driver.find_element(By.XPATH, self.btn_login_xpath).click()

    def click_register_as_new_user(self):
        self.driver.find_element(By.LINK_TEXT, self.register_as_new_user_text).click()

    def is_my_account_page_exists(self):
        try:
            return self.driver.find_element(By.XPATH, self.welcome_msg_xpath).is_displayed()
        except Exception:
            return False
