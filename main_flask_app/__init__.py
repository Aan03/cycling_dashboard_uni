from flask import Flask
from flask_marshmallow import Marshmallow
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, logout_user
import secrets
from flask_sqlalchemy import SQLAlchemy
import os
from main_flask_app.dash_app_cycling.stats import create_dash_app
from main_flask_app.dash_app_cycling import *
from main_flask_app.config import Config
from flask_marshmallow import Marshmallow

#Global Flask-marshmallow object
ma = Marshmallow()

# Create a connection to file as a SQLite database (this automatically creates the file if it doesn't exist)

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
secret_key = secrets.token_urlsafe(16)
print("\nSecret key for session:\n" + secret_key + "\n")

def page_not_found(e):
  return render_template('404.html'), 404

def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, "data/app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    
    from main_flask_app.models import Users
    with app.app_context():
        db.create_all()
    from main_flask_app.main_bp.main_bp import main_bp
    from main_flask_app.auth_bp.auth_bp import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    create_dash_app(app)

    ma.init_app(app) 


    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    

    app.register_error_handler(404, page_not_found)

    return app

app = create_flask_app()
from main_flask_app import models



if __name__ == '__main__':
    app.run(debug=True, threaded=True)