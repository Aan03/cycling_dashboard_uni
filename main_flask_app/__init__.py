from flask import Flask
from flask_marshmallow import Marshmallow
from flask import render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from main_flask_app.dash_app_cycling import *
from main_flask_app import config
from main_flask_app.data import csv_to_sql

csv_to_sql.creating_dataset_tables()

basedir = os.path.abspath(os.path.dirname(__file__))

# Global Flask_SQLAlchemy Object
db = SQLAlchemy()

# Engine and Base type declared allowing pre-existing dataset tables
# in the SQL database could be accessed and used
engine = create_engine(
    'sqlite:///' + os.path.join(basedir, "data/dataset_cycle_parking.db")
)
Base = declarative_base()
Base.metadata.reflect(engine)
db_dataset = scoped_session(sessionmaker(bind=engine))

# Global Flask_marshmallow object
ma = Marshmallow()

# The default page to be shown when a 404 error is given on the site
def page_not_found(e):
    return render_template('404.html'), 404

# The default page to be shown when a 500 error is given on the site
def internal_error(e):
    return render_template('500.html'), 500

def create_flask_app(config_selected):
    print(config_selected)
    app = Flask(__name__)
    app.config.from_object(config_selected)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    db.init_app(app)

    from main_flask_app.models import Users
    with app.app_context():
        db.create_all()

    # The blueprints needed to be imported first before being registered
    from main_flask_app.main_bp.main_bp import main_bp
    from main_flask_app.auth_bp.auth_bp import auth_bp
    from main_flask_app.api_bp.api_routes import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # The following was used to prevent a subroutine error where the dash
    # app server clashed with the flask server during testing.
    if str(config_selected) == "main_flask_app.config.Config":
        from main_flask_app.dash_app_cycling.dash_main import create_dash_app
        create_dash_app(app)

    # Marshmallow needed to be initialised after the SQLAlchemy database was
    ma.init_app(app)

    # Authentication setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app
from main_flask_app import models