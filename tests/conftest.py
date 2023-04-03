import pytest
from main_flask_app import create_flask_app, db
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from main_flask_app import config
import subprocess
import socket
import requests
import os
import sqlite3


@pytest.fixture(scope="function")
def app():
    """Create a Flask app configured for testing"""
    app = create_flask_app(config.TestConfig) 
    yield app


# An instance of the app is created as a test client.
# The test database used by the test using this fixture is cleared
# so for each new test, the users and reports are added again to an empty test
# database.
@pytest.fixture(scope="function")
def test_client(app):
    with app.app_context():   
        db.create_all()
    with app.test_client() as test_client:
        test_client.post("/api/user/sign_up",
                         json={"username": "test_user",
                               "password": "password123"})
        test_client.post("/api/user/sign_up",
                         json={"username": "test_user2",
                               "password": "password123"})
        test_client.post("/api/reports/create",
                         json={"username": "test_user",
                               "password": "password123",
                               "rack_id": "RWG148175",
                               "details": "test1 report details"})
        test_client.post("/api/reports/create",
                         json={"username": "test_user2",
                               "password": "password123",
                               "rack_id": "RWG015530",
                               "details": "test2 report details"})
        yield test_client
        db.drop_all()


@pytest.fixture(scope="function")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="function")
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
            url = f"http://localhost:{flask_port}"
            response = requests.get(url)
        except:
            print("There was an error connecting to the flask server")
    finally:
        server.terminate()
        

@pytest.fixture(scope="session")
def chrome_driver():
    """Setup options for the Chromedriver when using Selenium"""
    options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome("chromedriver.exe")
    yield driver


@pytest.fixture(scope="function")
def selenium_db_setup():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_file = (basedir + "/test.db")
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    drop_users_table = """DELETE FROM users;"""
    drop_reports_table = """DELETE FROM reports;"""
    cursor.execute(drop_users_table)
    connection.commit()
    cursor.execute(drop_reports_table)
    connection.commit()