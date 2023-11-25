import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def test_alert_window_fill_in_submit_btn():
    service = Service()
    ops = webdriver.ChromeOptions()
    ops.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=service, options=ops)

    driver.get("https://testautomationpractice.blogspot.com/")
    driver.maximize_window()

    alert_btn = driver.find_element(By.XPATH,
                                    "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/div/aside/div/div[3]/div[1]/button[3]")
    alert_btn.click()
    time.sleep(5)

    alert_window = driver.switch_to.alert
    assert alert_window.text == "Please enter your name:"
    alert_window.send_keys("Atanas")
    alert_window.accept()

    message = driver.find_element(By.XPATH,
                                  "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/div/aside/div/div[3]/div[1]/p").text
    expected_message = "Hello Atanas! How are you today?"
    assert expected_message == message


def test_alert_window_fill_in_cancel_btn():
    service = Service()
    driver = webdriver.Chrome(service=service)

    driver.get("https://testautomationpractice.blogspot.com/")
    driver.maximize_window()

    alert_btn = driver.find_element(By.XPATH,
                                    "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/div/aside/div/div[3]/div[1]/button[3]")
    alert_btn.click()
    time.sleep(5)

    alert_window = driver.switch_to.alert
    assert alert_window.text == "Please enter your name:"
    alert_window.send_keys("Atanas")
    alert_window.dismiss()

    message = driver.find_element(By.XPATH,
                                  "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/div/aside/div/div[3]/div[1]/p").text
    expected_message = "User cancelled the prompt."
    assert expected_message == message