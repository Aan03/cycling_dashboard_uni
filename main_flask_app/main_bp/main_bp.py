from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import UserMixin, current_user
from main_flask_app.dash_app_cycling import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
import csv
import os
import json
import pandas as pd
from main_flask_app import db
from main_flask_app.models import Users, Reports, Favourites

main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")
basedir = os.path.abspath(os.path.dirname(__file__))
maindir = os.path.abspath(os.path.join(basedir, os.pardir))



@main_bp.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@main_bp.route("/reports")
def reports_page():
    return render_template("reports.html")

myFile = open(maindir + "/data/cycle_parking_data.csv", "r")

reader = csv.DictReader(myFile)
myList = list()
for dictionary in reader:
    myList.append(dictionary)
markers_info = (myList)

rack_id_list = pd.read_csv(maindir + "/data/cycle_parking_data.csv", 
                           usecols = [0])

rack_id_list = rack_id_list.values.tolist()
rack_id_list = [elem for sublist in rack_id_list for elem in sublist]

myFile = open(maindir + "/data/cycle_parking_coordinates.csv", "r")
reader = csv.DictReader(myFile)
myList = list()
for dictionary in reader:
    myList.append(dictionary)    
markers = (myList)

myFile = open(maindir + "/data/boroughs_list.csv", "r")
reader = csv.reader(myFile)
myList = list()
for borough in reader:
    myList = myList + borough    
boroughs = (myList)

class ReportForm(FlaskForm):
    rack = StringField("Rack ID")#, validators=[DataRequired()])
    date = DateField("Date")#, validators=[DataRequired()])
    time = TimeField("Time")
    report_details = StringField("Report Details")
    submit = SubmitField("Submit")

@main_bp.route("/", methods=['POST', 'GET'])
def index():
    form = ReportForm()
    if request.method == "GET":
        return render_template('index.html', markers=json.dumps(markers), 
                           markers_info=json.dumps(markers_info), rack_id_list=rack_id_list,
                           boroughs = boroughs, form = form)
    
    elif request.method == "POST":
        reporter_id = current_user.id
        rack_id_flask = request.form['rack_id']
        date_flask = request.form['date']
        time_flask = request.form['time']
        report_details_flask = request.form['report_details']

        
        print(reporter_id, rack_id_flask, date_flask, time_flask, report_details_flask)

        new_report = Reports(reporter_id=reporter_id,rack_id=rack_id_flask, 
                             report_date=date_flask, 
                             report_time=time_flask, 
                             report_details=report_details_flask)
        
        try:
            db.session.add(new_report)
            db.session.commit()

            return redirect(url_for('main_bp.index'))

        except:
            return "error adding"


        