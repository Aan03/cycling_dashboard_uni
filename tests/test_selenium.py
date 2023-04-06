import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from main_flask_app.models import *
from tests.test_sel_db_generate import selenium_db_setup

existing_username = "existing_test_user"
existing_password = "test_raw_password"


def test_request_flask(run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed successfully
    THEN the status code will be 200
    """
    selenium_db_setup()
    time.sleep(5)
    url = f"http://localhost:{flask_port}/"
    time.sleep(10)
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("test_input", [(["test_new_selenium_user",
                                          "password123"])])
def test_sign_up_then_login(run_app_win, chrome_driver, flask_port, test_input):
    """
    Given a running app
    WHEN a user signs up
    AND then logins
    THEN the user should be logged in successfully 
         and be shown their personal reports page
    """
    selenium_db_setup()
    time.sleep(3)
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    sign_up_nav = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="nav-sign_up"]''')))
    sign_up_nav.click()
    username_sign_up_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_sign_up_entry.send_keys(test_input[0])
    password_sign_up_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_sign_up_entry.send_keys(test_input[1])
    chrome_driver.get_screenshot_as_file("screenshots/selenium_screenshots/signing_up.png")
    time.sleep(5)
    submit_sign_up = chrome_driver.find_element(By.XPATH,
                                                '''//*[@id="submit"]''')
    submit_sign_up.click()
    username_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_login_entry.send_keys(test_input[0])
    password_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_login_entry.send_keys(test_input[1])
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/logging_in.png")
    time.sleep(5)
    submit_sign_up = chrome_driver.find_element(By.XPATH,
                                                '''//*[@id="submit"]''')
    submit_sign_up.click()
    time.sleep(10)
    assert WebDriverWait(chrome_driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/h2"),
                                         'Welcome ' + test_input[0] + "."))


@pytest.mark.parametrize("test_input, expected",
                         [(["RWG148175", "Enfield", "test details"],
                           ["Report created successfully."]),
                          (["RWG14817a", "enfield", "test details"],
                           ["Please ensure that the rack ID "
                            "exists and is from the correct borough."
                            " Selecting the marker is the easiest way"
                            " to fill out the form correctly."]),
                          (["RWG148175", "wrong borough", "test details"],
                           ["Please ensure that borough is correct."
                            " Selecting the marker is the easiest way "
                            "to fill out the form correctly."])])
def test_create_report(run_app_win, chrome_driver, flask_port, test_input,
                       expected):
    """
    GIVEN a running app
    WHEN an existing user logs into their account (defined in fixture)
    AND then navigates to the main map page where they click on a
        map marker to fill the report form,
        and then edit the report form and submit it
    THEN the report should only be submitted to the database if it passes
    validation (the bike rack ID is real and the correct borough is entered)
    and the correct warning messages should be given.
    """
    selenium_db_setup()
    time.sleep(3)
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    login_nav = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="nav-login"]''')))
    login_nav.click()
    time.sleep(10)
    username_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_login_entry.send_keys(existing_username)
    time.sleep(2)
    password_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_login_entry.send_keys(existing_password)
    time.sleep(2)
    submit_login = chrome_driver.find_element(
        By.XPATH, '''//*[@id="submit"]''')
    submit_login.click()
    time.sleep(5)
    WebDriverWait(chrome_driver, 20).until(
        EC.text_to_be_present_in_element((
            By.XPATH, "/html/body/div/h2"),
            'Welcome ' + existing_username + "."))
    home_map_nav = chrome_driver.find_element(By.XPATH,
                                              '''//*[@id="nav-home"]''')

    home_map_nav.click()
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(EC.text_to_be_present_in_element(
        (By.XPATH, '//*[@id="map_side_options"]/h2'), 'Map Filters:'))
    main_map = WebDriverWait(chrome_driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH,
                                          '//*[@id="map_side_options"]/h2'),
                                         'Map Filters:'))
    main_map = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '''//*[@id="map"]/div[1]/div[3]/canvas''')
                                   ))
    main_map.click()
    time.sleep(5)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/clicked_map_marker.png")
    report_rack_id = chrome_driver.find_element(
        By.XPATH, '''//*[@id="report_rack_id"]''')
    report_borough = chrome_driver.find_element(
        By.XPATH, '''//*[@id="report_borough"]''')
    report_details = chrome_driver.find_element(
        By.XPATH, '''//*[@id="report_details"]''')
    time.sleep(5)
    report_rack_id.clear()
    report_rack_id.send_keys(test_input[0])
    report_rack_id.send_keys(Keys.ENTER)
    time.sleep(5)
    report_borough.clear()
    report_borough.send_keys(test_input[1])
    report_borough.send_keys(Keys.RETURN)
    time.sleep(5)
    submit_report = chrome_driver.find_element(
        By.XPATH, '//*[@id="report_submit"]')
    chrome_driver.execute_script("arguments[0].scrollIntoView();",
                                 submit_report)
    report_details.send_keys(test_input[2])
    time.sleep(5)
    report_details.send_keys(Keys.TAB)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/submitting_report.png")
    time.sleep(10)
    submit_report.click()
    time.sleep(5)
    WebDriverWait(chrome_driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '''/html/body/ul/li''')))
    assert WebDriverWait(chrome_driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '/html/body/ul/li'), expected[0]))


@pytest.mark.parametrize("test_input, expected",
                         [(["initial report details",
                            "edited report details"],
                           "Report details successfully edited.")])
def test_edit_report(run_app_win, chrome_driver, flask_port, test_input,
                     expected):
    """
    GIVEN a running app
    WHEN an existing user logs into their account (defined in fixture)
    AND then navigates to the main map page where they submit a
    report
    AND then goes to the "my reports" page where they edit the report
    details of the new report
    THEN the report should be edited successfully and a relevant flask flash
    message should be seen.
    """
    selenium_db_setup()
    time.sleep(3)
    username = existing_username
    password = existing_password
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(5)
    login_nav = WebDriverWait(chrome_driver, 20).until(
        EC.visibility_of_element_located((By.XPATH,
                                          '''//*[@id="nav-login"]''')))
    login_nav.click()
    time.sleep(10)
    username_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_login_entry.send_keys(username)
    password_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_login_entry.send_keys(password)
    time.sleep(2)
    submit_login = chrome_driver.find_element(By.XPATH,
                                              '''//*[@id="submit"]''')
    submit_login.click()
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(EC.text_to_be_present_in_element(
        (By.XPATH, "/html/body/div/h2"), 'Welcome ' + username + "."))
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/before_report_edit.png")
    first_report_edit = chrome_driver.find_element(
        By.XPATH, '//*[@id="editable_details1"]')
    first_report_edit.clear()
    first_report_edit.send_keys(test_input[1])

    confirm_edit_submit = chrome_driver.find_element(
        By.XPATH, '/html/body/div/table/tbody/tr[2]/td[7]/input')
    confirm_edit_submit.click()
    time.sleep(10)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/after_report_edit.png")
    assert WebDriverWait(chrome_driver, 15).until(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/ul/li'),
                                         expected))


@pytest.mark.parametrize("expected", [("Report successfully deleted.")])
def test_delete_report(run_app_win, chrome_driver, flask_port, expected):
    """
    GIVEN a running app
    WHEN an existing user logs into their account (defined in fixture)
    AND then navigates to the main map page where they submit a report
    AND then goes to the "my reports" page where they delete the new report
    THEN the report should be deleted successfully
    and a relevant flask flash message should be seen.
    """
    selenium_db_setup()
    time.sleep(3)
    username = existing_username
    password = existing_password
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    login_nav = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable(
           (By.XPATH, '''//*[@id="nav-login"]''')))
    login_nav.click()
    time.sleep(10)
    username_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_login_entry.send_keys(username)
    password_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_login_entry.send_keys(password)
    time.sleep(3)
    submit_login = chrome_driver.find_element(
        By.XPATH, '''//*[@id="submit"]''')
    submit_login.click()
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(
        EC.text_to_be_present_in_element(
           (By.XPATH, "/html/body/div/h2"), 'Welcome ' + username + "."))
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/before_report_deletion.png")
    report_delete = chrome_driver.find_element(
        By.XPATH, '/html/body/div/table/tbody/tr[2]/td[8]/input')
    report_delete.click()
    time.sleep(10)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/after_report_deletion.png")

    assert WebDriverWait(chrome_driver, 15).until(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/ul/li'),
                                         expected))


@pytest.mark.parametrize("test_input, expected",
                         [([existing_password],
                           ["Password changed successfully."]),
                          (["wrong password"],
                           ["Your current password was entered incorrectly. Try again."])])
def test_change_user_password(run_app_win, chrome_driver, flask_port,
                              test_input, expected):
    """
    GIVEN a running app
    WHEN an existing user logs into their account (defined in fixture)
    AND then navigates to the account page where they submit the form to
        change their password
    THEN the password should be changed successfully and a relevant flask
         flash message should be seen.
    """
    selenium_db_setup()
    time.sleep(3)
    username = existing_username
    password = existing_password
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    login_nav = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="nav-login"]''')))
    login_nav.click()
    time.sleep(10)
    username_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="username"]''')))
    username_login_entry.send_keys(username)
    password_login_entry = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="password"]''')))
    password_login_entry.send_keys(password)
    time.sleep(3)
    submit_login = chrome_driver.find_element(
        By.XPATH, '''//*[@id="submit"]''')
    submit_login.click()
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(EC.text_to_be_present_in_element(
        (By.XPATH, "/html/body/div/h2"), 'Welcome ' + username + "."))
    my_account_nav = chrome_driver.find_element(
        By.XPATH, '//*[@id="nav-my_account"]')
    my_account_nav.click()
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(EC.text_to_be_present_in_element(
        (By.XPATH, '/html/body/div/h3'), "Manage Your Account:"))
    time.sleep(3)
    current_password_entry = chrome_driver.find_element(
        By.XPATH, '//*[@id="password_current"]')
    current_password_entry.send_keys(test_input[0])
    new_password_entry = chrome_driver.find_element(
        By.XPATH, '//*[@id="password_new"]')
    new_password_entry.send_keys("new_test_password")
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/changing_password.png")

    changed_password_submit = chrome_driver.find_element(
        By.XPATH, '//*[@id="submit"]')
    changed_password_submit.click()

    time.sleep(10)

    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/password_changed.png")

    assert WebDriverWait(chrome_driver, 15).until(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/ul/li'),
                                         expected[0]))


def test_all_check_boxes_map(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN a user clicks through the different map filter check boxes
    THEN the map should change to reflect those filters
         (screenshots saved in tests/selenium_screenshots)
    """
    selenium_db_setup()
    time.sleep(3)
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)

    WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '''//*[@id="map"]/div[1]/div[3]/canvas''')
                                   ))

    covered_check_box = chrome_driver.find_element(
        By.XPATH, '//*[@id="covered_box"]')
    secured_check_box = chrome_driver.find_element(
        By.XPATH, '//*[@id="secured_box"]')
    locker_check_box = chrome_driver.find_element(
        By.XPATH, '//*[@id="locker_box"]')

    covered_check_box.click()
    time.sleep(5)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/covered_filter.png")
    secured_check_box.click()
    time.sleep(5)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/secured_filter.png")
    locker_check_box.click()
    time.sleep(5)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/locker_filter.png")


@pytest.mark.parametrize("test_input, expected",
                         [("my_reports", "Please log in to access this page."),
                          ("account", "Please log in to access this page.")])
def test_login_warning(run_app_win, chrome_driver, flask_port, test_input,
                       expected):
    """
    GIVE a running app
    WHEN an anonymous (not logged in) user goes to the "my reports" or
    "manage account" page (which are only for logged in users)
    THEN the user should be redirected to the login page and be shown a
    flask flash warning to login.
    """
    url = f"http://localhost:{flask_port}/" + test_input
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    WebDriverWait(chrome_driver, 20).until(
        EC.visibility_of_element_located(
           (By.XPATH, '''/html/body/div/div/h3''')))
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/login_warning.png")
    time.sleep(10)
    assert WebDriverWait(chrome_driver, 15).until(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/ul/li'),
                                         expected))


def test_page_not_found(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN a user goes to a page that does not exist
    THEN the user should be redirected to the pre-defined "404.html" page.
    """
    url = f"http://localhost:{flask_port}/" + "not_a_page"
    time.sleep(10)
    chrome_driver.get(url)
    time.sleep(5)
    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/404_error.png")
    assert WebDriverWait(chrome_driver, 15).until(
        EC.text_to_be_present_in_element((By.XPATH, '/html/body/div/h2'),
                                         "404: Page not found"))


def test_all_reports_page_selected(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-reports"]
    THEN a page with the title "All User Theft Reports:" should be displayed
    AND the page should contain an element with the xpath /html/body/div/h5
        should be displayed and contain a text value "There is currently 1
        active theft report."
    """
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    nav_all_reports_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='nav-reports']")
    )
    nav_all_reports_button.click()
    time.sleep(10)
    title_element = chrome_driver.find_element(
        By.XPATH, "//h2[contains(text(), 'All User Theft Reports:')]")
    assert title_element.is_displayed()
    report_count_element = chrome_driver.find_element(
        By.XPATH, "/html/body/div/h5")
    assert report_count_element.is_displayed()
    assert report_count_element.text == "There is currently 1 active theft report."


def test_download_data_empty(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN a user goes to the "download data" page
    AND chooses to download the reports from a borough with no data/reports
    available
    THEN a flask flash message will appear telling the user that there is no
    data for that borough, and they will be redirected to the same page.
    """
    url = f"http://localhost:{flask_port}/download_data"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    borough_dropdown = WebDriverWait(
        chrome_driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '''//*[@id="report_borough"]''')))

    borough_dropdown.click()
    borough_dropdown.send_keys("l")
    borough_dropdown.send_keys(Keys.ENTER)
    download_submit = chrome_driver.find_element(
        By.XPATH, "/html/body/div/form/button")
    download_submit.click()
    time.sleep(10)
    flash_no_data = WebDriverWait(
        chrome_driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '''/html/body/ul/li''')))

    chrome_driver.get_screenshot_as_file(
        "screenshots/selenium_screenshots/no_reports_download.png")

    assert "There are no related active reports in" in flash_no_data.text
    assert WebDriverWait(chrome_driver, 20).until(
        EC.visibility_of_element_located(
        (By.XPATH, '''/html/body/div/h2'''))).text == "Download Reports"


def test_download_data_page(run_app_win, chrome_driver, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-download_reports"]
    THEN a page with the title "Download Reports" should be displayed
    AND the page should contain an element with the xpath
    /html/body/div/form/button should be displayed and
    contain a text value "Download Reports:"
    """
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    nav_download_reports_button = WebDriverWait(
        chrome_driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-download_reports"]')
    )
    time.sleep(5)
    nav_download_reports_button.click()
    time.sleep(10)
    text = chrome_driver.find_element(
        By.XPATH, "/html/body/div/h2").text
    assert "Download Reports" in text


def test_api_instructions_page_selected(run_app_win, chrome_driver,
                                        flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the //*[@id="nav-home"]
    THEN a page with the title "Cycling Parking API Instructions:" should be
        displayed
    AND the page should contain an element with the xpath /html/body/div/h5[1]
    should be displayed and contain a text value "API GET Routes:"

    """
    url = f"http://localhost:{flask_port}/"
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    nav_api_button = WebDriverWait(chrome_driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '''//*[@id="nav-api"]''')))
    nav_api_button.click()
    time.sleep(10)
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
    time.sleep(5)
    chrome_driver.get(url)
    time.sleep(10)
    nav_login_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="nav-login"]')
    )
    nav_login_button.click()
    time.sleep(10)
    text = chrome_driver.find_element(By.XPATH, "/html/body/div/div/h3")
    assert "Login:" in text.text
