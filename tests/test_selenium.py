import subprocess
import socket
import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port

@pytest.fixture(scope="module")
def run_app_win(flask_port):
    """Runs the Flask app for live server testing on Windows"""
    server = subprocess.Popen(
        [
            "flask",
            "--app",
            "main_flask_app:create_flask_app('main_flask_app.config.TestConfig')",
            "run",
            "--port",
            str(flask_port)
        ]
    )
    try:
        yield server
        try:
            url = f"http://localhost:{flask_port}/api"
            response = requests.get(url)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(response)
        except:
            print("nopeeeeeeeee")
    finally:
        server.terminate()

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