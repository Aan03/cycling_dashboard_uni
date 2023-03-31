import pytest
from main_flask_app import create_flask_app, db
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from main_flask_app import config

@pytest.fixture(scope="function")
def app():
    """Create a Flask app configured for testing"""
    app = create_flask_app(config.TestConfig)
    yield app

@pytest.fixture(scope="function")
def test_client(app):
    with app.app_context():   
        db.create_all()
    with app.test_client() as test_client:
        test_client.post("/api/user/sign_up", json = {"username" : "test_user",
                                                      "password" : "password123"})
        test_client.post("/api/user/sign_up", json = {"username" : "test_user2",
                                                      "password" : "password123"})
        test_client.post("/api/reports/create", json = {"username" : "test_user",
                                                      "password" : "password123",
                                                      "rack_id" : "RWG148175",
                                                      "details" : "test1 report details"})
        test_client.post("/api/reports/create", json = {"username" : "test_user2",
                                                      "password" : "password123",
                                                      "rack_id" : "RWG015530",
                                                      "details" : "test2 report details"})
        yield test_client
        db.drop_all()

@pytest.fixture(scope="session")
def chrome_driver():
    """Setup options for the Chromedriver when using Selenium"""
    options = Options()
    #options.add_argument("--no-sandbox")
    #options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    #options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome("chromedriver.exe")
    yield driver