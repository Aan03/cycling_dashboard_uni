import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.firefox.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

def pytest_setup_options():
    """Setup options for the Chromedriver when using Selenium"""
    options = Options()
    #options.add_argument("--no-sandbox")
    #options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    return options