from flask_login import UserMixin
from main_flask_app import db

#import bcrypt to hash passwords


class user(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

<<<<<<< HEAD
class reports(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    report = db.Column(db.String(1000))
    report_date = db.Column(db.String(1000))
    report_time = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    
=======
>>>>>>> 4550cb4e1a8097c667544f2db72255c03c7e74c7

class favourites(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    favourite = db.Column(db.String(100))

<<<<<<< HEAD
=======




>>>>>>> 4550cb4e1a8097c667544f2db72255c03c7e74c7
