from flask_login import UserMixin
from main_flask_app import db


#import bcrypt to hash passwords


class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))

class reports(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    rack_id = db.Column(db.String(1000))
    report_details = db.Column(db.String(1000))
    report_date = db.Column(db.Date)
    report_time = db.Column(db.String(1000))

    

class favourites(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    username = db.Column(db.String(1000))
    rack_id = db.Column(db.String(1000))