from flask import Flask

from flask_login import LoginManager
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, logout_user

import secrets
from flask_sqlalchemy import SQLAlchemy
import os
from main_flask_app.dash_app_cycling.stats import create_dash_app
from main_flask_app.dash_app_cycling import *
from main_flask_app.config import Config
from sqlalchemy import create_engine, types

from flask_marshmallow import Marshmallow

#Global Flask-marshmallow object
ma = Marshmallow()

# Create a connection to file as a SQLite database (this automatically creates the file if it doesn't exist)

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
db = SQLAlchemy()
secret_key = secrets.token_urlsafe(16)

def create_flask_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = secret_key
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, "data/app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    #ma.init_app(app)
    #create_engine("sqlite:///" + str(db_path), echo=False)
    from main_flask_app.models import user, favourites
    #from main_flask_app.models import user
    with app.app_context():
        db.create_all()
    from main_flask_app.main_bp.main_bp import main_bp
    from main_flask_app.auth_bp.auth_bp import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    create_dash_app(app)

    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))

    return app

app = create_flask_app()
from main_flask_app import models

if __name__ == '__main__':
    app.run(debug=True, threaded=True)