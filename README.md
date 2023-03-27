# COMP0034 Coursework 2

1. Run the flask app from the \comp0034-cw2-g-team11 directory and use the following commands:

pip install -r requirements.txt
flask --app main_flask_app --debug run

2. There are two blueprints being used, auth_bp and main_bp. Auth_bp manages the account creation and management of users, while main_bp handles everything else.

3. The Flask app is initialised in the __init__.py file. The dash app from COMP0034-CW1 has also been added in as a page.

4. User authorisation has been setup with SHA256 encryption for passwords. Users can create theft reports which can be viewed by other users. Users can also edit or delete their reports. Users are also able to change their passwords.

5. When creating the main app, a library called Leaflet was used, the neccesasary map marker variables and information were loaded in using Flask.

6. All forms were made using Flask.

7. The dataset is stored on the "cycling_app.db" file and loaded from there when needed.

8. The API is used on the site by grabbing report data (for a specific borough or all borough) and creating a downloadable CSV file with that data.