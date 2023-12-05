from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support.select import Select


class MyAccountPage:
    home_btn_text = 'Home'
    events_btn_id = 'dropdownMenuLink'
    hello_msg_xpath = '/html/body/header/nav/div/div/ul[1]/li[1]/a'
    logout_btn_xpath = '/html/body/header/nav/div/div/ul[1]/li[2]/form/button'
    welcome_msg_xpath = '/html/body/div/main/div/h1'
    view_all_events_text = 'all events'
    new_event_text = 'new event'
    all_events_link_text = 'All Events'
    create_event_link_text = 'Create Event'

    def __init__(self, driver):
        self.driver = driver

    def click_home_btn(self):
        self.driver.find_element(By.LINK_TEXT, self.home_btn_text).click()

    def click_events_link(self):
        event_btn = self.driver.find_element(By.ID, self.events_btn_id)
        event_btn.click()

    def click_all_events(self):
        all_events_link = self.driver.find_element(By.LINK_TEXT, self.all_events_link_text)
        all_events_link.click()

    def click_logout(self):
        logout_link = self.driver.find_element(By.XPATH, self.logout_btn_xpath)
        logout_link.click()
