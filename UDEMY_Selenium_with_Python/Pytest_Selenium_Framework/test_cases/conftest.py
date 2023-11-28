import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture()
def setup(request):
    browser = request.config.getoption("--browser")

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif browser == 'edge':
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise ValueError(f"Invalid browser specified: {browser}")

    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Specify the browser (chrome/firefox/edge)")


@pytest.fixture()
def browser(request):
    return request.config.getoption('--browser')


########################### pytest HTML Report #############################

def pytest_configure(config):
    config._metadata['Project Name'] = 'SoftUni QA'
    config._metadata['Module Name'] = 'CustRegistration'
    config._metadata['Tester'] = 'Atanas Stankin'


@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop('Plugins', None)

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = os.path.abspath(os.curdir)+'\\reports\\'+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+".html"