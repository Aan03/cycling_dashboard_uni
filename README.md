# COMP0034 Coursework 2

1. Run the flask app from the \comp0034-cw2-g-team11 directory and use the following command:

flask --app main_flask_app --debug runs

2. There are two blueprints being used, auth_bp and main_bp. Auth_bp manages the account creation and management of users, while main_bp handles everything else.

3. The Flask app is initialised in the __init__.py file. The dash app from COMP0034-CW1 has also been added in as a page.

4. User authorisation has been setup with SHA256 encryption for passwords. Users can create theft reports which can be viewed by other users. Users can also edit or delete their reports.

5. When creating the main app, a library called Leaflet was used, the neccesasary map marker variables and information were loaded in using Flask.

6. All forms were made using Flask.