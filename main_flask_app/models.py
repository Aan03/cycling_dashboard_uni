from flask_login import UserMixin
from main_flask_app import db

#import bcrypt to hash passwords


class user(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class reports(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    report = db.Column(db.String(1000))
    report_date = db.Column(db.String(1000))
    report_time = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    

class favourites(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    favourite = db.Column(db.String(100))