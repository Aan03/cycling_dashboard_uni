from flask import Blueprint, render_template
from main_flask_app.dash_app_cycling import *
import csv
import os
import json
main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

@main_bp.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@main_bp.route("/reports")
def reports():
    return render_template("reports.html")

@main_bp.route("/")
def index():
    myFile = open(basedir + "/templates/cycle_parking_coordinates.csv", "r")
    reader = csv.DictReader(myFile)
    myList = list()
    for dictionary in reader:
        myList.append(dictionary)    
    markers = (myList)
    return render_template('index.html', markers=json.dumps(markers))