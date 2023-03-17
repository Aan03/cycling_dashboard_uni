from flask_login import UserMixin
from main_flask_app import db
from main_flask_app import ma
#import bcrypt to hash passwords


class user(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class favourites(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))
    #email = db.Column(db.String(100), unique=True)
    favourite = db.Column(db.String(100))


class ReportsSchema(ma.SQLALchemySchema):
""" Marshmallow schema defining the attributes for creating reports."""

class Meta:
model = 