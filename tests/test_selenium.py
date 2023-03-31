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

def test_home_page_running(run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed successfully
    THEN the status code will be 200
    """
    # localhost has the IP address 127.0.0.1, which refers
    # back to your own server on your local computer
    url = f"http://localhost:{flask_port}/"
    response = requests.get(url)
    assert response.status_code == 200


def test_dash_statistics_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-dashboard"]
    THEN a page with the title "Density distribution and proportion of bike racks in all boroughs" should be displayed
    AND the page should contain an element with the xpath //*[@id="react-entry-point"]/div/div[1]/div/div/p[1]
    should be displayed and contain a text value "Select a rack type:"
    AND the page should contain an element with the xpath //*[@id="htid"]
    should be displayed and contain the text "Hover over any area to see statistics"

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)

    nav_dash_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='nav-dashboard']")
    )
    nav_dash_button.click()
    title_element = chrome_driver.find_element(By.XPATH, "//h2[contains(text(), 'Density distribution and proportion of bike racks in all boroughs')]")
    assert title_element.is_displayed()
    report_count_element = chrome_driver.find_element(By.XPATH, "//*[@id='react-entry-point']/div/div[1]/div/div/p[1]")
    assert report_count_element.is_displayed()
    assert report_count_element.text == "Select a rack type:"
    htid_element = chrome_driver.find_element(By.XPATH, "//*[@id='htid']")
    assert htid_element.is_displayed()
    assert htid_element.text == "Hover over any area to see statistics"


def test_All_Reports_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-reports"]
    THEN a page with the title "All User Theft Reports:" should be displayed
    AND the page should contain an element with the xpath /html/body/div/h5
    should be displayed and contain a text value "There are currently 5 active theft reports."

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    nav_All_Reports_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='nav-reports']")
    )
    nav_All_Reports_button.click()
    title_element = chrome_driver.find_element(By.XPATH, "//h2[contains(text(), 'All User Theft Reports:')]")
    assert title_element.is_displayed()
    report_count_element = chrome_driver.find_element(By.XPATH, "//h5[contains(text(), 'There are currently')]")
    assert report_count_element.is_displayed()
    assert report_count_element.text == "There are currently 5 active theft reports."


def test_Download_Data_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-download_reports"]
    THEN a page with the title "Download Reports" should be displayed
    AND the page should contain an element with the xpath /html/body/div/form/button
    should be displayed and contain a text value "Download Reports:"

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)

    nav_download_reports_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-download_reports"]')
    )
    nav_download_reports_button.click()
    text = chrome_driver.find_element(By.XPATH, "/html/body/div/form/button").text
    assert "Download Reports:" in text


def test_API_Instructions_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-home"]
    THEN a page with the title "Cycling Parking API Instructions:" should be displayed
    AND the page should contain an element with the xpath /html/body/div/h5[1]
    should be displayed and contain a text value "API GET Routes:"

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)

    nav_home_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-home"]')
    )
    nav_home_button.click()
    text = chrome_driver.find_element(By.XPATH, "/html/body/div/h5[1]").text
    assert "API GET Routes:" in text


def test_Login_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the xpath //*[@id="nav-login"]
    THEN a page with the title "Login:" should be displayed
    AND the page should contain an element with the xpath //*[@id="username"]
    should be displayed

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)

    nav_home_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-home"]')
    )
    nav_home_button.click()
    text = chrome_driver.find_element(By.XPATH, "/html/body/div/h5[1]").text
    assert "API GET Routes:" in text


def test_Sign_Up_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the xpath //*[@id="nav-sign_up"]
    THEN a page with the title "Sign Up:" should be displayed
    AND the page should contain an element with the xpath //*[@id="username"]
    should be displayed

    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)

    nav_sign_up_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-sign_up"]')
    )
    nav_sign_up_button.click()
    text = chrome_driver.find_element(By.XPATH, "/html/body/div/h5[1]").text
    assert "Sign Up:" in text

    username_field = chrome_driver.find_element(By.XPATH, '//*[@id="username"]')
    assert username_field.is_displayed()



