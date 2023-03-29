import pytest
from main_flask_app import create_flask_app, db
from flask import Response
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

@pytest.fixture(scope="session")
def test_client():
    flask_app = create_flask_app()
    with flask_app.app_context():   
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context 
        db.create_all()
    flask_app.config.update({'TESTING': True})
    with flask_app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope="function")
def chrome_browser():
    """Setup options for the Chromedriver when using Selenium"""
    options = Options()
    #options.add_argument("--no-sandbox")
    #options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome("chromedriver.exe")
    yield driver