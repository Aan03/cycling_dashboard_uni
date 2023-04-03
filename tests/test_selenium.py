import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
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

@pytest.mark.parametrize("test_input", [(["test_new_selenium_user", "password123"])])
def test_sign_up_then_login(run_app_win, selenium_db_setup, chrome_driver, flask_port, test_input, expected):
    """
    GIVEN a running app
    WHEN the homepage is accessed successfully
    THEN the status code will be 200
    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    sign_up_nav = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="nav-sign_up"]''')))
    time.sleep(1)
    sign_up_nav.click()
    username_sign_up_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="username"]''')))
    username_sign_up_entry.send_keys(test_input[0])
    password_sign_up_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="password"]''')))
    password_sign_up_entry.send_keys(test_input[1])
    time.sleep(1)
    submit_sign_up = chrome_driver.find_element(By.XPATH, '''//*[@id="submit"]''')
    submit_sign_up.click()
    username_login_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="username"]''')))
    username_login_entry.send_keys(test_input[0])
    password_login_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="password"]''')))
    password_login_entry.send_keys(test_input[1])
    time.sleep(1)
    submit_sign_up = chrome_driver.find_element(By.XPATH, '''//*[@id="submit"]''')
    submit_sign_up.click()
    
    assert WebDriverWait(chrome_driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/h2"), 'Welcome '+ test_input[0] + "."))



@pytest.mark.parametrize("test_input, expected", [(["RWG148175", "Enfield", "test details"], ["Report created successfully."]),
                                                  (["RWG14817a", "enfield", "test details"], ['''Please ensure that the rack ID exists and 
                                                                                                is from the correct borough.''']),
                                                  (["RWG148175", "wrong borough", "test details"], ['''Please ensure that the rack ID exists and 
                                                                                                is from the correct borough.'''])])
def test_create_report(run_app_win, selenium_db_setup, chrome_driver, flask_port, test_input, expected):
    """
    GIVEN a running app
    WHEN the homepage is accessed successfully
    THEN the status code will be 200
    """
    username = "test_new_selenium_user"
    password = "password123"
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    sign_up_nav = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="nav-sign_up"]''')))
    time.sleep(1)
    sign_up_nav.click()
    username_sign_up_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="username"]''')))
    username_sign_up_entry.send_keys(username)
    password_sign_up_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="password"]''')))
    password_sign_up_entry.send_keys(password)
    time.sleep(1)
    submit_sign_up = chrome_driver.find_element(By.XPATH, '''//*[@id="submit"]''')
    submit_sign_up.click()
    username_login_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="username"]''')))
    username_login_entry.send_keys(username)
    password_login_entry = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="password"]''')))
    password_login_entry.send_keys(password)
    time.sleep(1)
    submit_sign_up = chrome_driver.find_element(By.XPATH, '''//*[@id="submit"]''')
    submit_sign_up.click()
    WebDriverWait(chrome_driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/h2"), 'Welcome '+ username + "."))

    home_map_nav = chrome_driver.find_element(By.XPATH, '''//*[@id="nav-home"]''')
    home_map_nav.click()

    WebDriverWait(chrome_driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="map_side_options"]/h2'), 'Map Filters:'))

    main_map = WebDriverWait(chrome_driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="map_side_options"]/h2'), 'Map Filters:'))

    main_map = WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''//*[@id="map"]/div[1]/div[3]/canvas''')))
    main_map.click()

    time.sleep(1)

    report_rack_id = chrome_driver.find_element(By.XPATH, '''//*[@id="report_rack_id"]''')
    report_borough = chrome_driver.find_element(By.XPATH, '''//*[@id="report_borough"]''')
    report_details = chrome_driver.find_element(By.XPATH, '''//*[@id="report_details"]''')

    time.sleep(10)


    #report_rack_id.clear()
    #report_rack_id.send_keys(test_input[0])
    #report_rack_id.send_keys(Keys.ENTER)

    #report_borough.clear()
    #report_borough.send_keys(test_input[1])
    #report_borough.send_keys(Keys.RETURN)

    submit_report = chrome_driver.find_element(By.XPATH,'//*[@id="report_submit"]')
    chrome_driver.execute_script("arguments[0].scrollIntoView();", submit_report)

    report_details.send_keys(test_input[2])
    time.sleep(3)
    report_details.send_keys(Keys.TAB)

    time.sleep(3)

    submit_report.click()



    
    
    #submit_report.send_keys(Keys.RETURN)

    #WebDriverWait(chrome_driver,20).until(EC.visibility_of_element_located((By.XPATH,'''/html/body/ul/li''')))

    assert WebDriverWait(chrome_driver, 15).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/ul/li'), expected[0]))










def test_all_reports_page_selected(run_app_win, chrome_driver, flask_port):
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
    nav_all_Reports_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='nav-reports']")
    )
    nav_all_Reports_button.click()
    title_element = chrome_driver.find_element(By.XPATH, "//h2[contains(text(), 'All User Theft Reports:')]")
    assert title_element.is_displayed()
    report_count_element = chrome_driver.find_element(By.XPATH, "//h5[contains(text(), 'There are currently')]")
    assert report_count_element.is_displayed()
    assert report_count_element.text == "There are currently 5 active theft reports."


def test_download_data_page_selected(run_app_win, chrome_driver, flask_port):
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


def test_api_instructions_page_selected(run_app_win, chrome_driver, flask_port):
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


def test_login_page_selected(run_app_win, chrome_driver, flask_port):
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