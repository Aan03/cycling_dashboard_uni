from flask_login import UserMixin
from main_flask_app import db


#import bcrypt to hash passwords


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary key
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    reports = db.relationship("Reports", back_populates="user")
    favourites = db.relationship("Favourites", back_populates="user")
    
    

class Reports(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True) # primary key
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id")) # foreign key
    rack_id = db.Column(db.String(9))
    report_date = db.Column(db.String(1000))
    report_time = db.Column(db.String(1000))
    report_details = db.Column(db.String(1000))
    user = db.relationship("Users", back_populates="reports")

class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True) # primary key
    user_favourited_id = db.Column(db.Integer, db.ForeignKey("users.id")) # foreign key
    username = db.Column(db.String(1000))
    rack_id = db.Column(db.String(1000))
    user = db.relationship("Users", back_populates="favourites")