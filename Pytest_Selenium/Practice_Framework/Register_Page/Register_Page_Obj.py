from selenium.webdriver.common.by import By


class RegisterPage:
    input_first_name_id = 'input-firstname'
    input_last_name_id = 'input-lastname'
    input_email_id = 'input-email'
    input_password_id = 'input-password'
    btn_radio_yes_id = 'input-newsletter-yes'
    btn_radio_no_id = 'input-newsletter-no'
    check_agree_xpath = '//*[@id="form-register"]/div/div/div/input'
    btn_continue_xpath = '/html/body/main/div[2]/div/div/form/div/div/button'

    def __init__(self, driver):
        self.driver = driver

    def set_first_name(self, first_name):
        first_name_field = self.driver.find_element(By.ID, self.input_first_name_id)
        first_name_field.clear()
        first_name_field.send_keys(first_name)

    def set_last_name(self, last_name):
        last_name_field = self.driver.find_element(By.ID, self.input_last_name_id)
        last_name_field.clear()
        last_name_field.send_keys(last_name)

    def set_email(self, email):
        email_field = self.driver.find_element(By.ID, self.input_email_id)
        email_field.clear()
        email_field.send_keys(email)

    def set_password(self, password):
        password_field = self.driver.find_element(By.ID, self.input_password_id)
        password_field.clear()
        password_field.send_keys(password)

    def set_radio_subscribe(self, command):
        if command == "Yes":
            radio_btn = self.driver.find_element(By.ID, self.btn_radio_yes_id)
            radio_btn.click()
        elif command == 'No':
            radio_btn = self.driver.find_element(By.ID, self.btn_radio_no_id)
            radio_btn.click()

    def check_agree(self):
        checkbox = self.driver.find_element(By.XPATH, self.check_agree_xpath)
        checkbox.click()

    def click_continue(self):
        continue_btn = self.driver.find_element(By.XPATH, self.btn_continue_xpath)
        continue_btn.click()