from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Register_Page.Register_Page_Obj import RegisterPage


class TestLogin:
    def test_register(self):
        serv_obj = Service("C:/Users/user/Downloads/edgedriver_win64/msedgedriver.exe")
        # self.driver = webdriver.Chrome(service=serv_obj)
        self.driver = webdriver.Edge(service=serv_obj)
        self.driver.get("https://demo.opencart.com/index.php?route=account/register&language=en-gb")
        self.driver.maximize_window()

        self.register_page = RegisterPage(self.driver)
        self.register_page.set_last_name('Atanas')
        self.register_page.set_last_name('Stankin')
        self.register_page.set_email('somemail@abv.bg')
        self.register_page.set_password('Password123')
        self.register_page.set_radio_subscribe('No')
        self.register_page.check_agree()
        self.register_page.click_continue()
        self.act_tite = self.driver.title
        self.driver.close()
        assert self.act_tite == "Register Account"
