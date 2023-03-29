import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen
from flask import url_for, Response, request
import pytest

#GET - get all reports
@pytest.mark.parametrize("test_input, expected", [("", 200), ("s", 404)])
def test_get_reports_all(test_client, test_input, expected):
    response = test_client.get("/api/reports" + test_input)
    assert response.status_code == expected

#GET - get all reports for a specific borough
@pytest.mark.parametrize("test_input, expected", [("Enfield", 200), ("not a borough", 404),
                                                   ("tower hamlets", 200), ("lewisham", 200)])
def test_get_reports_borough(test_client, test_input, expected):
    response = test_client.get("/api/reports/borough/" + test_input)
    assert response.status_code == expected

#GET - get all reports for a specific bike rack ID
@pytest.mark.parametrize("test_input, expected", [("RWG148175", 200), ("not a rack", 404),
                                                   ("rwg148175", 200), ("RWG1481", 404)])
def test_get_reports_rack(test_client, test_input, expected):
    response = test_client.get("/api/reports/rack/" + test_input)
    assert response.status_code == expected

#GET - get all reports for a specific user
@pytest.mark.parametrize("test_input, expected", [("testuser", 200), ("not_a_user", 404)])
def test_get_reports_user(test_client, test_input, expected):
    response = test_client.get("/api/reports/user/" + test_input)
    assert response.status_code == expected

#POST - create a new report
@pytest.mark.parametrize("test_input, expected", [(["testuser", "123", "RWG148175", "test"], 
                                                   [201, "Theft report added successfully."]),
                                                   (["testuser", "12", "RWG148175", "test"], 
                                                   [200, "Password recieved was incorrect."]),
                                                  (["not_a_user", "123", "RWG148175", "test"], 
                                                   [404, "does not exist."]),
                                                   (["testuser", "123", "RWG1481", "test"], 
                                                   [404, "A bike rack with that ID was not found."])])
def test_post_report_create(test_client, test_input, expected):
    response = test_client.post("/api/reports/create", json = {"username" : test_input[0], 
                                                               "password" : test_input[1],
                                                                "rack_id" : test_input[2], 
                                                                "details"  : test_input[3]})
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in response.json 
    
def test_post_report_createee(test_client):
    response = test_client.post("/api/reports/create", json = {"username" : "testuser", "password" : "123", "rack_id" : "RWG148175", "details" : "test"})
    print(response.data)
    assert response.status_code == 201


#DELETE - delete a report for a specific user
@pytest.mark.parametrize("test_input, expected", [(1, 200), (100, 404)])
def test_delete_reports_user(test_client, test_input, expected):
    response = test_client.get("/api/reports/delete/" + str(test_input))
    assert response.status_code == expected

'''
#POST - create a new report
@pytest.mark.parametrize("test_input, expected", [("Enfield", 200), ("not a borough", 404),
                                                   ("tower hamlets", 200), ("lewisham", 200)])
def test_get_reports_borough(test_client, test_input, expected):
    response = test_client.get("/api/reports/borough/" + test_input)
    assert response.status_code == expected
'''




    


'''
def test_home_page22(test_client, chrome_browser):
    with app.app_context():
        chrome_browser.get(url_for("main_bp.index"))
        WebDriverWait(chrome_browser,20)
    assert 2==2'''
