from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import UserMixin, login_required, current_user
from sqlalchemy import desc
from main_flask_app.dash_app_cycling import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, validators
import csv
import os
import json
import pandas as pd
from main_flask_app import db
from main_flask_app.models import Users, Reports
from main_flask_app.schemas import ReportsSchema
from flask import make_response
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, validators
import itertools

reports_schema = ReportsSchema(many=True)
reports_schema = ReportsSchema()

main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")
basedir = os.path.abspath(os.path.dirname(__file__))
maindir = os.path.abspath(os.path.join(basedir, os.pardir))

@main_bp.route('/my_reports', methods=['POST', 'GET'])
@login_required
def my_reports():
    reports_table = Reports.query.order_by(Reports.report_date.desc(), Reports.report_time.desc())
    user_reports_count = Reports.query.filter_by(reporter_id = current_user.id).count()
    if request.method == "GET":
        return render_template('my_reports.html', reports_table = reports_table, 
                               user_reports_count = user_reports_count)
    
    elif request.method == "POST":
        flash("Tested")
        return render_template('my_reports.html', reports_table = reports_table)

    
@main_bp.route("/edit_report_details/<int:report_id>", methods=['POST'])
@login_required
def edit_report_details(report_id):
    if request.method == "POST":
        report_to_edit = Reports.query.filter_by(id=report_id).first()
        if report_to_edit.reporter_id == current_user.id:
            print('editable_details' + str(report_id))
            report_to_edit.report_details = request.form['editable_details' + str(report_id)]
            db.session.commit()
            flash("Report details successfully edited.")
            return redirect(url_for("main_bp.my_reports"))
        else:
            flash("There was an error editing the report details. Please try again later.")
            return redirect(url_for("main_bp.my_reports"))

@main_bp.route("/delete_report/<int:report_id>", methods=['POST'])
@login_required
def delete_report(report_id):
    if request.method == "POST":
        report_to_delete = Reports.query.filter_by(id=report_id).first()
        if report_to_delete.reporter_id == current_user.id:
            Reports.query.filter_by(id=report_id).delete()
            db.session.commit()
            flash("Report successfully deleted.")
            return redirect(url_for("main_bp.my_reports"))
        else:
            flash("There was an error deleting the report. Please try again later.")
            return redirect(url_for("main_bp.my_reports"))

@main_bp.route("/dash_statistics")
def dash():
    return render_template("dash_statistics.html")

@main_bp.route("/reports")
def reports_page():
    reports_table = Reports.query.order_by(Reports.report_date.desc(), Reports.report_time.desc())
    return render_template("reports.html", reports_table=reports_table)

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
    report_rack_id = StringField("Rack ID", validators = [validators.Length(min=9, max=9), validators.DataRequired()])
    report_borough = StringField("Borough", validators = [validators.DataRequired()])
    report_date = DateField("Date", validators = [validators.DataRequired()])
    report_time = TimeField("Time", validators = [validators.DataRequired()])
    report_details = StringField("Report Details", validators = [validators.DataRequired(), validators.Regexp(r'^[\w.@+-]+$')])
    report_submit = SubmitField("Submit")

@main_bp.route("/", methods=['POST', 'GET'])
def index():
    report_form = ReportForm()
    if request.method == "GET":
        return render_template('index.html', markers=json.dumps(markers), 
                           markers_info=json.dumps(markers_info), rack_id_list=rack_id_list,
                           boroughs = boroughs, report_form = report_form)
    
    elif request.method == "POST":
        reporter_id = current_user.id
        rack_id_flask = request.form['report_rack_id']
        borough_flask = request.form['report_borough']
        date_flask = request.form['report_date']
        time_flask = request.form['report_time']
        report_details_flask = request.form['report_details']

    
        new_report = Reports(reporter_id=reporter_id,
                             report_borough=borough_flask,
                             rack_id=rack_id_flask, 
                             report_date=date_flask, 
                             report_time=time_flask, 
                             report_details=report_details_flask)
        
        try:
            db.session.add(new_report)
            db.session.commit()
            return redirect(url_for('main_bp.index'))

        except:
            flash("There was an error submitting the report. Please try again later.")
            return redirect(url_for('main_bp.index'))
        

class BoroughForm(FlaskForm):
    report_borough = StringField("Borough", validators=[validators.DataRequired()])

@main_bp.route("/download_data", methods=['POST', 'GET'])
def download_data():
    print("download_data function called")
    # Open the CSV file and read the boroughs
    with open(maindir + "/data/boroughs_list.csv", "r") as file:
        reader = csv.reader(file)
        print(file)
        boroughs = list(itertools.chain.from_iterable(reader))
        print(boroughs)

    # Create the borough selection form
    form = BoroughForm()
    print("before form.validate_on_submit function called")    
    if form.validate_on_submit():
        print("after form.validate_on_submit function called")
        # Get the selected borough from the form data
        selected_borough = form.report_borough.data
        print(f"Selected borough: {selected_borough}")

        # Query the database for reports in the selected borough
        reports_filtered = Reports.query.filter_by(report_borough=selected_borough).all()
        print(f"Reports: {reports_filtered}")

        # If no reports are found, flash a message and redirect back to the reports page
        if not reports_filtered:
            flash("No reports found for selected borough.")
            return redirect(url_for("main_bp.download_data"))

        # Convert the reports data to a CSV string
        csv_data = StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['id', 'reporter_id', 'borough', 'date', 'time', 'details'])
        for report in reports_filtered:
            writer.writerow([report.id, report.reporter_id, report.report_borough, report.report_date, report.report_time, report.report_details])

        # Create a response with the CSV data and appropriate headers
        response = make_response(csv_data.getvalue())
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = f"attachment; filename={selected_borough}_reports.csv"

        # Return the response for downloading the CSV file
        return response

    # Render the download_reports template with the borough selection form
    print("download_data function called")
    return render_template('download_data.html', form=form, boroughs=boroughs)

"""    
class BoroughForm(FlaskForm):
    report_borough = StringField("Borough", validators=[validators.DataRequired()])

@main_bp.route("/download_data", methods=['POST', 'GET'])
def download_data():
    print("download_data function called")
    # Open the CSV file and read the boroughs
    with open(maindir + "/data/boroughs_list.csv", "r") as file:
        reader = csv.reader(file)
        print(file)
        boroughs = list(itertools.chain.from_iterable(reader))

    # Create the borough selection form
    form = BoroughForm()
    
    if form.validate_on_submit():
        print("form.validate_on_submit function called")
        # Get the selected borough from the form data
        selected_borough = form.report_borough.data
        print(f"Selected borough: {selected_borough}")

        # Query the database for reports in the selected borough
        reports = Reports.query.filter_by(report_borough=selected_borough).all()
        print(f"Reports: {reports}")

        # If no reports are found, flash a message and redirect back to the reports page
        if not reports:
            flash("No reports found for selected borough.")
            return redirect(url_for("main_bp.download_data"))

        # Convert the reports data to a CSV string
        csv_data = StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['id', 'reporter_id', 'borough', 'date', 'time', 'details'])
        for report in reports:
            writer.writerow([report.id, report.reporter_id, report.report_borough, report.report_date, report.report_time, report.report_details])

        # Create a response with the CSV data and appropriate headers
        response = make_response(csv_data.getvalue())
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = f"attachment; filename={selected_borough}_reports.csv"

        # Return the response for downloading the CSV file
        return response

    # Render the download_reports template with the borough selection form
    print("download_data function called")
    return render_template('download_data.html', form=form, boroughs=boroughs)

"""    



"""
@main_bp.route("/download_reports", methods=["POST"])
def download_reports(reports_table):
    # Get a list of boroughs from a CSV file
    with open(maindir + "/data/boroughs_list.csv", "r") as f:
        boroughs = [row[0] for row in csv.reader(f)]

    # Extract the selected borough from the form data
    borough = request.form.get("borough_select")
    print("Selected borough:", borough)

    # Return a 404 code if the region is not found in the database
    reports = db.session.query(Reports).filter_by(report_borough=borough).all()
    reports_json = reports_schema.dump(reports)

    # Convert the JSON data to a CSV string
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    if reports_json:
        writer.writerow(reports_json[0].keys())
        for report in reports_json:
            writer.writerow(report.values())
    else:
        # handle the case where there are no reports for the selected borough
        flash("No reports found for selected borough.")
        return redirect(url_for("main_bp.reports"))

    # Create a response with the CSV data and appropriate headers
    response = make_response(csv_data.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment; filename={borough}_reports.csv"

    # Render the downloading_reports template with the boroughs list as context
    return render_template("reports.html", reports_table=reports_table, boroughs=boroughs)
"""