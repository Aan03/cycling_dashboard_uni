from flask import Flask
from flask_marshmallow import Marshmallow
from flask import render_template
from flask_login import LoginManager
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from main_flask_app.dash_app_cycling.stats import create_dash_app
from main_flask_app.dash_app_cycling import *
from main_flask_app.config import Config
from main_flask_app.data import csv_to_sql
from flask_marshmallow import Marshmallow


csv_to_sql.creating_dataset_tables()

basedir = os.path.abspath(os.path.dirname(__file__))

secret_key = secrets.token_urlsafe(16)
print("\nSecret key for session:\n" + secret_key + "\n")

#Global Flask_SQLAlchemy object
db = SQLAlchemy()

#Engine and Base type declared so that pre-existing dataset tables in the SQL database
# could be accessed and used
engine = create_engine('sqlite:///' + os.path.join(basedir, 
                                                   "data/cycle_parking.db"))
Base = declarative_base()
Base.metadata.reflect(engine)
db_session = scoped_session(sessionmaker(bind=engine))

#Global Flask_marshmallow object
ma = Marshmallow()

#The default page to be shown when a 404 error is given on the site
def page_not_found(e):
  return render_template('404.html'), 404

def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "data/cycle_parking.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.register_error_handler(404, page_not_found)

    db.init_app(app)
    
    from main_flask_app.models import Users
    with app.app_context():
        db.create_all()

    #The blueprints needed to be imported first before being registered
    from main_flask_app.main_bp.main_bp import main_bp
    from main_flask_app.auth_bp.auth_bp import auth_bp
    from main_flask_app.api_bp.api_routes import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    create_dash_app(app)

    #Marshmallow needed to be initialised after the SQLAlchemy database was
    ma.init_app(app)

    #Authentication setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app

app = create_flask_app()
from main_flask_app import models

if __name__ == '__main__':
    app.run(debug=True, threaded=True)