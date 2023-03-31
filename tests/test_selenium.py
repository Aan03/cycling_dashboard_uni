import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.action_chains import ActionChains


def test_request_flask(run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed successfully
    THEN the status code will be 200
    """
    url = f"http://localhost:{flask_port}/"
    response = requests.get(url)
    assert response.status_code == 200


def test_home_page(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the id="1"
    THEN a page with the title "Rome" should be displayed
    AND 
    """
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    # Wait until the element with id="1" is on the page
    # https://www.selenium.dev/documentation/webdriver/waits/ and then click on it