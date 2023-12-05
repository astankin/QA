from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class AccountRegistrationPage:
    input_username_id = 'Input_Username'
    input_email_id = 'Input_Email'
    input_password_id = 'Input_Password'
    input_conf_password_id = 'Input_ConfirmPassword'
    input_first_name_id = 'Input_FirstName'
    input_last_name_id = 'Input_LastName'
    btn_register_css_selector = "button[type='submit'].btn.btn-primary"
    conf_msg_class_name = 'text-center'
    error_message_xpath = '/html/body/div/main/div/div/form/div[1]/ul/li'
    register_link_xpath = '/html/body/header/nav/div/div/ul[1]/li[1]/a'

    def __init__(self, driver):
        self.driver = driver

    def set_username(self, username):
        self.driver.find_element(By.ID, self.input_username_id).send_keys(username)

    def set_first_name(self, f_name):
        self.driver.find_element(By.ID, self.input_first_name_id).send_keys(f_name)

    def set_last_name(self, l_name):
        self.driver.find_element(By.ID, self.input_last_name_id).send_keys(l_name)

    def set_email(self, email):
        self.driver.find_element(By.ID, self.input_email_id).send_keys(email)

    def set_telephone(self, telephone):
        self.driver.find_element(By.NAME, self.txt_telephone).send_keys(telephone)

    def set_password(self, password):
        self.driver.find_element(By.ID, self.input_password_id).send_keys(password)

    def set_confirm_password(self, conf_pass):
        self.driver.find_element(By.ID, self.input_conf_password_id).send_keys(conf_pass)

    def click_continue(self):
        self.driver.find_element(By.XPATH, self.btn_continue_xpath).click()

    def click_register(self):
        self.driver.find_element(By.CSS_SELECTOR, self.btn_register_css_selector).click()

    def get_confirm_msg(self):
        self.element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.conf_msg_class_name))
        )
        self.h1_text = self.element.text
        return self.h1_text

    def get_error_message(self):
        return self.driver.find_element(By.XPATH, self.error_message_xpath)

    def click_register_link(self):
        self.driver.find_element(By.XPATH, self.register_link_xpath).click()

    def register(self, username, email, password, confirm_pass, first_name, last_name):
        self.set_username(username)
        self.set_email(email)
        self.set_password(password)
        self.set_confirm_password(confirm_pass)
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.click_register()

