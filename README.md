# COMP0034 Coursework 2

### This README contains:

[- General information on the flask app and API](#general-information)  
[- Walk through of the flask website/app usage](#example-usage-of-flask-app)  
[- API Routes](#api-routes)  
[- Testing](#testing)

## General information
1. Run the following commands from the main [/comp0034-cw2-g-team11](/) directory:

    pip install -r requirements.txt
    flask --app main_flask_app --debug run

2. There are three blueprints being used, [auth_bp](main_flask_app/auth_bp/), [main_bp](main_flask_app/main_bp/) and [api_bp](main_flask_app/api_bp/). Auth_bp manages the account creation and management of users, while main_bp handles the rest of the user experience like viewing, creating and managing theft reports. The api_bp manages the API routes.

3. The Flask app is initialised in the __init__.py file.

4. User authorisation has been setup with SHA256 encryption for passwords. Users can create theft reports which can be viewed by other users. Users can also edit or delete their reports. Users are also able to change their passwords.

5. When creating the main app, a library called Leaflet was used, the neccesasary map marker variables and information were loaded in using Flask.

6. All forms were made using Flask.

7. The dataset is stored on the [cycle_parking.db](/main_flask_app/data/cycle_parking.db) database file and loaded from there when needed. In this case it is reloaded each time the flask server starts with the [csv_to_sql.py](/main_flask_app/data/csv_to_sql.py) being used to make sure the dataset is available in SQL form (it does not need to be reloaded in reality but if the database file or dataset tables are missing it ensures that they are available when the server runs). The engine and base type needed to be declared too in SQLAlchemy in order for the dataset tables to be accessed by flask.

8. The API has GET, POST, PUT and DELETE routes. It allows for the creation of users and the creation, deletion and editing of reports. Some screenshots taken during tesing on the API testing website "Postman.co" can be found in the [API Postman.co screenshots folder.](/screenshots/api_postman.co_screenshots/). All the API routes can be found in the [api_bp/api_routes.py](/main_flask_app/api_bp/api_routes.py) file.

9. The API is used on the site by grabbing report data (for a specific borough or all borough) and creating a downloadable CSV file with that data.

10. The [dash app](/main_flask_app/dash_app_cycling/) from COMP0034-CW1 has also been added in as a page.

11. Different configurations are used for normal operations and for testing purposes. These can be found in the [main_flask_app/config.py](/main_flask_app/config.py) file.

## Example usage of flask app

Home view (not logged in):  
![Usage #1](https://github.com/ucl-comp0035/comp0034-cw2-g-team_11/blob/main/screenshots/site_app_usage_screenshots/1_index_page.PNG)

All reports page:  
![Usage #2](https://github.com/ucl-comp0035/comp0034-cw2-g-team_11/blob/main/screenshots/site_app_usage_screenshots/2_all_user_reports.PNG)

Download reports page which uses API to get reports (downloaded file shown):  
![Usage #3](/screenshots/site_app_usage_screenshots/3_download_reports.png)  

Dash statistics page:  
![Usage #4](/screenshots/site_app_usage_screenshots/4_dash_statistics.png)  

Sign up page:  
![Usage #5](/screenshots/site_app_usage_screenshots/5_sign_up.png)  

Login page:  
![Usage #6](/screenshots/site_app_usage_screenshots/6_login.png)  

Page shown after logging in:  
![Usage #7](/screenshots/site_app_usage_screenshots/7_logged_in.png)

Logged in view of home page showing the map. Users can click on markers to start reports:  
![Usage #8](/screenshots/site_app_usage_screenshots/8_report_map.png)  

Users can manage reports (edit details or delete them):
![Usage #9](/screenshots/site_app_usage_screenshots/9_manage_reports.png)

Users can change their passwords:  
![Usage #10](/screenshots/site_app_usage_screenshots/10_change_password.png)  

Anyone can view reports for specific bike racks:
![Usage #11](/screenshots/site_app_usage_screenshots/11_specific_reports.png)  

## API Routes
This information is also available on the website itself on the API Instructions page.

### API GET Routes:
http://127.0.0.1:5000/api/reports - Get all reports.

http://127.0.0.1:5000/api/reports/borough/(Enter borough name) - Get all reports for a specific borough.

http://127.0.0.1:5000/api/reports/rack/(Enter rack ID) - Get all reports for a specific bike rack.

http://127.0.0.1:5000/api/reports/user/(Enter username) - Get all reports made by a specific user.

### API POST Routes:
http://127.0.0.1:5000/api/reports/create - Create a new report.  
JSON request body format for this request:  
{"username" : "Enter username of report creator",  
"password" : "Enter password of report creator",  
"rack_id" : "Enter bike rack ID",  
"details" : "Enter report details"}

http://127.0.0.1:5000/api/user/sign_up  
Sign up a new user.  
JSON request body format for this request:  
{"username" : "Enter username",  
"password" : "Enter password"}

### API PUT Routes:

http://127.0.0.1:5000/api/reports/edit/[Enter report ID] - Edit an existing report.  
JSON request body format for this request:  
{"username" : "Enter username of report creator",  
"password" : "Enter password of report creator",  
"details" : "Enter new/updated report details"}

http://127.0.0.1:5000/api/user/change_password - Changing a current user's password.  
JSON request body format for this request:  
{"username" : "Enter username",  
"current_password" : "Enter current password",  
"new_password" : "Enter new password"}

### API DELETE Routes:

http://127.0.0.1:5000/api/reports/delete/[Enter report ID]  
Delete an existing report.  
JSON request body format for this request:  
{"username" : "[Enter username of report creator]",  
"password" : "[Enter password of report creator]"}

## Testing
1. Run the following command from the main [/comp0034-cw2-g-team11](/) directory to initiate testing:

    pytest -v --cov=main_flask_app  

2. The tests for the API routes can be found in the [testing/test_api.py](/testing/test_api.py) file.

3. A copy of the clean [cycle_parking.db](/main_flask_app/data/cycle_parking.db) database file is used for testing purposes. This test database is the [test.db](/testing/test.db) file.