from flask_login import UserMixin
from main_flask_app import db, Base


class cycle_parking_data(Base):
    __table__ = Base.metadata.tables['cycle_parking_data']


class boroughs_list(Base):
    __table__ = Base.metadata.tables['boroughs_list']


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    reports = db.relationship("Reports", back_populates="user")


class Reports(db.Model):
    __tablename__ = 'reports'
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    # foreign key
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rack_id = db.Column(db.String(9))
    report_date = db.Column(db.String(1000))
    report_borough = db.Column(db.String(1000))
    report_time = db.Column(db.String(1000))
    report_details = db.Column(db.String(1000))
    user = db.relationship("Users", back_populates="reports")
