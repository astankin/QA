import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def test_alert_window_fill_in_submit_btn():
    service = Service()
    driver = webdriver.Chrome(service=service)

    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    driver.maximize_window()
    time.sleep(5)

