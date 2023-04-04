import pytest
from urllib.request import urlopen
from flask import url_for, Response, request


# auth.bp routes
@pytest.mark.parametrize("test_input, expected", [(["test_user", "password123"], "Welcome test_user."), 
                                                  (["test_user", "wrong password"],"Please check your login details and try again."),
                                                  (["not_a_user", "password123"], "Please check your login details and try again.")])
def test_correct_login(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN an existing user logins using the login form
     THEN check that the user is logged in successfully.
     """
     response = test_client.post(
      '/login',
      data = dict(username=test_input[0], password=test_input[1]),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


@pytest.mark.parametrize("test_input, expected", [("test_user", "Username is taken. Please enter another one."), 
                                                  ("not_a_user", "Login")])
def test_correct_sign_up(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a new user signs up using a username that is not taken
     THEN check that the user was signed up or refused if the username was taken.
     """
     response = test_client.post(
      '/sign_up',
      data = dict(username=test_input, password="password123"),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


@pytest.mark.parametrize("test_input, expected", [("password123", "Password changed successfully."), 
                                                  ("wrong password", "Your current password was entered incorrectly. Try again.")])
def test_correct_change_password(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a user signs in and then changes their password
     THEN check that the password was changed successfully. 
     """
     test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )

     response = test_client.post(
      '/account',
      data = dict(password_current=test_input, password_new="new_password"),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


# main.bp routes
@pytest.mark.parametrize("test_input, expected", [(["RWG148175", "Enfield"], "Report created successfully."), 
                                                  (["RWG148175", "wrong borough"], "Please ensure that borough is correct."),
                                                  (["wrong bike rack ID", "Enfield"], 
                                                  "Please ensure that the rack ID exists and is from the correct borough.")])
def test_correct_report_creation(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a user signs in and submits a report
     THEN check that the report form was successfully filled out and if not then flash the
          correct warning messages. 
     """
     test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )

     response = test_client.post(
      '/',
      data = dict(report_rack_id=test_input[0],
                  report_borough=test_input[1],
                  report_date="2023-04-04",
                  report_time="23:00", 
                  report_details="test details"),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


@pytest.mark.parametrize("test_input, expected", [("Lambeth", "There are no related active reports in Lambeth")])
def test_correct_data_downloaded(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a user downloads report data for a specific borough
     THEN check that correct flask flashes are shown if there is no data
          available and hence no downloadable file available. 
     """
     test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )

     response = test_client.post(
      '/download_data',
      data = dict(report_borough=test_input),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


@pytest.mark.parametrize("expected", [("Manage/View Your Submitted Theft Reports:")])
def test_correct_my_reports(test_client, expected):
     """
     GIVEN a Flask application
     WHEN a user logins and is directed to the my_reports page 
     THEN check that their own reports are shown.
     """
     response = test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)


@pytest.mark.parametrize("test_input, expected", [("1", "Report successfully deleted.")])
def test_correct_delete_report(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a user logins and deletes a report they created on the my_reports page 
     THEN check that the report was deleted and that the correct flash message was given.
     """
     test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )
     
     response = test_client.post(
      '/delete_report/' + test_input,
      data = dict(reporter_id=1),
      follow_redirects=True
      )
     print(response.data)
     assert str(expected) in str(response.data)



# All get content tests
def test_correct_logout(test_client):
     """
     GIVEN a Flask application
     WHEN a user signs in and afterwards logouts
     THEN check that the user was logged out successfully.
     """
     test_client.post(
      '/login',
      data = dict(username="test_user", password="password123"),
      follow_redirects=True
      )

     response = test_client.get(
      '/logout',
      follow_redirects=True)
     print(response.data)
     assert str("Logged out successfully.") in str(response.data)


def test_index_content(test_client):
     """
     GIVEN a Flask application
     WHEN the '/' home page is requested
     THEN check the response contains 'Sign up or login to submit and manage theft reports.'.
     """
     response = test_client.get('/')    
     assert b'Map Filters' in response.data
     assert b'Sign up or login to submit and manage theft reports.' in response.data


def test_dash_statistics_content(test_client):
     """
     GIVEN a Flask application
     WHEN the dash statistics page is requested
     THEN check the response contains the correct dash iframe.
     """
     response = test_client.get('/dash_statistics')    
     print(response.data)
     assert b'iframe src="http://localhost:5000/dash_app' in response.data


def test_all_reports_content(test_client):
     """
     GIVEN a Flask application
     WHEN the reports page is requested
     THEN check that the response contains 'All User Theft Reports:'.
     """
     response = test_client.get('/reports')    
     print(response.data)
     assert b'All User Theft Reports:' in response.data


@pytest.mark.parametrize("test_input, expected", [("RWG148175", "active theft report for RWG148175"),
                                                  ("RWG015530", "active theft report for RWG015530" )])
def test_specific_reports_content(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN the page for the reports on a specific bike rack is requested
     THEN check that the response contains the active theft reports for the correct bike rack.
     """
     response = test_client.get('/specific_reports/' + str(test_input))    
     print(response.data)
     assert expected in str(response.data)


def test_download_data_content(test_client):
     """
     GIVEN a Flask application
     WHEN the download data page is requested
     THEN check that the response contains "Download Reports".
     """
     response = test_client.get('/download_data')    
     print(response.data)
     assert b'Download Reports' in response.data


@pytest.mark.parametrize("test_input", [("api_instructions"), ("api")])
def test_api_instructions_content(test_client, test_input):
     """
     GIVEN a Flask application
     WHEN the api page is requested using either path
     THEN check that the response contains the api instructions.
     """
     response = test_client.get('/' + str(test_input))    
     print(response.data)
     assert b'Cycling Parking API Instructions:' in response.data


@pytest.mark.parametrize("test_input, expected", [("login", "Login"), 
                                                  ("sign_up", "Sign Up:")])
def test_login_sign_up_content(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN the login and sign up pages are requested
     THEN check that the response contains the relevant login or sign up form.
     """
     response = test_client.get('/' + str(test_input))    
     print(response.data)
     assert (expected) in str(response.data)


@pytest.mark.parametrize("test_input, expected", [("not_a_page", "404"), 
                                                  ("null", "404")])
def test_error_content(test_client, test_input, expected):
     """
     GIVEN a Flask application
     WHEN a non-existing page is requested
     THEN check that the response is the 404 error page.
     """
     response = test_client.get('/' + str(test_input))
     assert str(expected) in str(response.data)


def test_my_reports_logged_out_content(test_client):
     """
     GIVEN a Flask application
     WHEN the my reports page is requested by a logged out user
     THEN check the response contains the message: "Please log in to access this page.".
     """
     response = test_client.get('/my_reports',
                                follow_redirects=True)    
     assert b'Please log in to access this page.' in response.data