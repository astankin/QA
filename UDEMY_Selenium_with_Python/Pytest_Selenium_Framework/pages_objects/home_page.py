from selenium.webdriver.common.by import By


class HomePage():
    my_account_xpath = "//*[@id='top']/div[2]/div[2]/ul/li[2]/div/a"
    register_link_txt = 'Register'
    login_link_txt = 'Login'

    def __init__(self, driver):
        self.driver = driver

    def click_my_account(self):
        self.driver.find_element(By.XPATH, self.my_account_xpath).click()

    def click_register(self):
        self.driver.find_element(By.LINK_TEXT, self.register_link_txt).click()

    def click_login(self):
        self.driver.find_element(By.LINK_TEXT, self.login_link_txt).click()