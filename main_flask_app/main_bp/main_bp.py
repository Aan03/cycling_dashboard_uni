from flask import Blueprint, render_template
from main_flask_app.dash_app_cycling import *
import csv
import os
import json
main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")
basedir = os.path.abspath(os.path.dirname(__file__))
maindir = os.path.abspath(os.path.join(basedir, os.pardir))

@main_bp.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@main_bp.route("/reports")
def reports():
    return render_template("reports.html")


myFile = open(maindir + "/data/cycle_parking_data.csv", "r")
reader = csv.DictReader(myFile)
myList = list()
for dictionary in reader:
    myList.append(dictionary)
markers_info = (myList)

myFile = open(maindir + "/data/cycle_parking_coordinates.csv", "r")
reader = csv.DictReader(myFile)
myList = list()
for dictionary in reader:
    myList.append(dictionary)    
markers = (myList)

@main_bp.route("/", methods=['POST', 'GET'])
def index():
    messages = [{'title': 'Message One',
                 'date': 'Message One',
                 'time': 'Message One',
             'content': 'Message One Content'},
            ]
    return render_template('index.html', markers=json.dumps(markers), 
                           markers_info=json.dumps(markers_info), 
                           messages = messages)