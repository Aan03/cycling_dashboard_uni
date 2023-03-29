import pytest
from urllib.request import urlopen
from flask import url_for, Response, request

#GET - get all reports
@pytest.mark.parametrize("test_input, expected", [("", 200), ("s", 404)])
def test_get_reports_all(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a GET request for all reports,
    THEN the user should receive a JSON response containing all user reports 
         and they should also receive a response code of 200.
         Or they should receive a response code of 404 if the request was invalid.
    '''
    response = test_client.get("/api/reports" + test_input)
    assert response.status_code == expected

#GET - get all reports for a specific borough
@pytest.mark.parametrize("test_input, expected", [("Enfield", [200, "report"]),
                                                  ("eNFIELD", [200, "report"]), 
                                                  ("not a borough", [404, "The borough name is incorrect"]),
                                                  ("tower hamlets", [200, "report"]), 
                                                  ("lewisham", [200, "report"])])

def test_get_reports_borough(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a GET request for all reports from a specific borough,
    THEN the user should receive a JSON response containing all user reports from that borough 
         and they should also receive a response code of 200.
         Or they should receive a response code of 404 if the request was invalid.
    '''
    response = test_client.get("/api/reports/borough/" + test_input)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#GET - get all reports for a specific bike rack ID
@pytest.mark.parametrize("test_input, expected", [("RWG148175", [200, "report"]), 
                                                  ("not a rack", [404, "The bike rack ID is incorrect"]),
                                                  ("rwg148175", [200, "report"]), 
                                                  ("RWG1481", [404, "The bike rack ID is incorrect"])])

def test_get_reports_rack(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a GET request for all reports made for a specific bike rack,
    THEN the user should receive a JSON response containing all user reports made for
         that specified bike rack and they should also receive a response code of 200.
         Or they should receive a response code of 404 if the request was invalid.
    '''
    response = test_client.get("/api/reports/rack/" + test_input)
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#GET - get all reports for a specific user
@pytest.mark.parametrize("test_input, expected", [("test_user", [200, "report"]), 
                                                  ("not_a_user", [404, "does not exist."])])

def test_get_reports_user(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a GET request for all reports made by a specific user,
    THEN the user should receive a JSON response containing all user reports made by 
         that specified user and they should also receive a response code of 200.
         Or they should receive a response code of 404 if the request was invalid.
    '''
    response = test_client.get("/api/reports/user/" + test_input)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#POST - create a new report
@pytest.mark.parametrize("test_input, expected", [(["test_user", "password123", "RWG014970", "test"], 
                                                   [201, "Theft report added successfully."]),
                                                  (["test_user", "wrong_password", "RWG148175", "test"], 
                                                   [200, "Password received was incorrect."]),
                                                  (["not_a_user", "123", "RWG148175", "test"], 
                                                   [404, "does not exist."]),
                                                  (["test_user", "password123", "RWG1481", "test"], 
                                                   [404, "A bike rack with that ID was not found."])])

def test_post_report_create(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a POST request to create a new report,
    THEN the user should receive a response code of 201 if the new report is successfully created,
        200 if the user credentials are incorrect to show acknowledgement, or 404 if the 
        user or bike rack doesn't exist.
    '''
    response = test_client.post("/api/reports/create", json = {"username" : test_input[0], 
                                                               "password" : test_input[1],
                                                                "rack_id" : test_input[2], 
                                                                "details"  : test_input[3]})
    
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in response.json 
    
#POST - sign up a new user
@pytest.mark.parametrize("test_input, expected", [(["test_user", "password123"], [200, "already exists"]),
                                                  (["new_test_user", "password123"], [201, "has been signed up successfuly."])])
def test_post_sign_up(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a POST request is made to sign up a new user,
    THEN the user should receive a response code of 201 if the user is signed up successfully,
         or 200 if the username is taken.
    '''
    response = test_client.post("/api/user/sign_up", json = {"username" : test_input[0],
                                                               "password" : test_input[1]})
    
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#PUT - change report details
@pytest.mark.parametrize("test_input, expected", [([1, "test_user", "password123", "updated details"], [200, "successfully edited."]),
                                                  ([1, "test_user", "wrong password", "updated details"], [200, "Password received was incorrect."]),
                                                  ([1, "test_user2", "password123", "updated details"], [200, "under a different username."]),
                                                  ([1, "not_a_user", "password123", "updated details"], [404, " does not exist."]),
                                                  ([100, "test_user", "password123", "updated details"], [404, "that ID does not exist."])])
def test_put_edit_details(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a PUT request is made to edit the details of an existing theft report,
    THEN the user should receive a response code of 200 if the theft report edit is successful,
        200 if the request is received but the user credentials are incorrect,
        or 404 if the user or report don't exist.
    '''
    response = test_client.put("/api/reports/edit/" + str(test_input[0]), json = {"username" : test_input[1],
                                                                              "password" : test_input[2],
                                                                              "details" : test_input[3]})
    
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#PUT - change user password
@pytest.mark.parametrize("test_input, expected", [(["test_user", "password123", "updatedpassword"], [200, "Password changed successfully."]),
                                                  (["test_user", "wrong password", "updatedpassword"], [200, "Current password received was incorrect."]),
                                                  (["not_a_user", "password123", "updatedpassword"], [404, "does not exist."])])

def test_put_change_password(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a PUT request is made to change the password of an existing user,
    THEN the user should receive a response code of 200 if the password change is successful,
        200 if the request is received but the user entered their current password incorrectly,
        or 404 if the user doesn't exist.
    '''
    response = test_client.put("/api/user/change_password", json = {"username" : test_input[0],
                                                                    "current_password" : test_input[1],
                                                                    "new_password" : test_input[2]})
    
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)

#DELETE - delete a report for a specific user
@pytest.mark.parametrize("test_input, expected", [([1, "test_user", "password123"], [200, "Report deleted successfully."]), 
                                                  ([1, "test_user", "wrong password"], [200, "Password received was incorrect."]),
                                                  ([2, "test_user", "password123"], [200, "does exist but under a different username."]),
                                                  ([1, "test_user2", "password123"], [200, "does exist but under a different username."]),
                                                  ([100, "test_user", "password123"], [404, "A report with that ID does not exist."]),
                                                  ([1, "not_a_user", "password123"], [404, "does not exist."])])

def test_delete_report(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a DELETE request is made to delete an existing report,
    THEN the user should receive a response code of 200 if the report deletion is successful,
        200 if the request is received but the user entered their credentials incorrectly,
        or 404 if the report or user don't exist.
    '''
    response = test_client.delete("/api/reports/delete/" + str(test_input[0]), json = {"username" : test_input[1],
                                                                                       "password" : test_input[2]})
    print(response.data)
    assert response.status_code == expected[0]
    assert expected[1] in str(response.data)