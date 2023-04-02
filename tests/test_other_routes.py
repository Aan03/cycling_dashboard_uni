import pytest
from urllib.request import urlopen
from flask import url_for, Response, request


# GET - get all reports
@pytest.mark.parametrize("test_input, expected", [("", 200), ("s", 404)])
def test_get_reports_all(test_client, test_input, expected):
    '''
    GIVEN that the API server is running,
    WHEN a user makes a GET request for all reports,
    THEN the user should receive a JSON response containing all user reports
         and they should also receive a response code of 200.
         Or they should receive a response code of 404 if the request
         was invalid.
    '''
    response = test_client.get("/api/reports" + test_input)
    assert response.status_code == expected