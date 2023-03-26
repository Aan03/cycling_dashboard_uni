from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import UserMixin, login_required, current_user
from main_flask_app.dash_app_cycling import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, validators
import csv
import os
import json
import pandas as pd
from main_flask_app import db, db_session
from main_flask_app.models import Users, Reports, cycle_parking_data, boroughs_list

main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")
basedir = os.path.abspath(os.path.dirname(__file__))
maindir = os.path.abspath(os.path.join(basedir, os.pardir))

new_boroughs = []
for x in db_session.query(boroughs_list.borough):
    new_boroughs.append(list(x))
new_boroughs = [element for nestedlist in new_boroughs for element in nestedlist]

feature_id_list = []
marker_data = []
for x in db_session.query(cycle_parking_data.feature_id, cycle_parking_data.prk_cover,
                          cycle_parking_data.prk_secure, cycle_parking_data.prk_locker,
                          cycle_parking_data.prk_cpt, cycle_parking_data.borough,
                          cycle_parking_data.photo1_url, cycle_parking_data.photo2_url,
                          cycle_parking_data.latitude, cycle_parking_data.longitude):
    rack_type_converted = []
    for i in range(1,4):
        if x[i] == "1":
            rack_type_converted.append("True")
        if x[i] == "0":
            rack_type_converted.append("False")
    each_row = {"feature_id":x[0],
                "prk_cover":rack_type_converted[0],
                "prk_secure":rack_type_converted[1],
                "prk_locker":rack_type_converted[2],
                "prk_cpt":x[4],
                "borough":x[5],
                "photo1_url":x[6],
                "photo2_url":x[7],
                "latitude":x[8],
                "longitude":x[9]
                }
    marker_data.append(each_row)
    feature_id_list.append(x[0])

class ReportForm(FlaskForm):
    report_rack_id = StringField("Rack ID", validators = [validators.Length(min=9, max=9), validators.DataRequired()])
    report_borough = StringField("Borough", validators = [validators.DataRequired()])
    report_date = DateField("Date", validators = [validators.DataRequired()])
    report_time = TimeField("Time", validators = [validators.DataRequired()])
    report_details = StringField("Report Details", validators = [validators.DataRequired(), validators.Regexp(r'^[\w.@+-]+$')])
    report_submit = SubmitField("Submit")

@main_bp.route('/my_reports', methods=['POST', 'GET'])
@login_required
def my_reports():
    reports_table = Reports.query.order_by(Reports.report_date.desc(), Reports.report_time.desc())
    user_reports_count = Reports.query.filter_by(reporter_id = current_user.id).count()
    if request.method == "GET":
        return render_template('my_reports.html', reports_table = reports_table, 
                               user_reports_count = user_reports_count)
    
    elif request.method == "POST":
        flash("Your reports have been updated.")
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
    user_reports_count = Reports.query.count()
    return render_template("reports.html", reports_table=reports_table, 
                           user_reports_count = user_reports_count)

@main_bp.route("/", methods=['POST', 'GET'])
def index():
    report_form = ReportForm()
    if request.method == "GET":
        return render_template('index.html', 
                           markers_info=json.dumps(marker_data), boroughs = new_boroughs,
                           report_form = report_form)
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
        
@main_bp.route("/specific_reports/<string:specific_rack_id>", methods=['GET'])
def specific_reports(specific_rack_id):
    if request.method == "GET":
        if specific_rack_id in feature_id_list:
            specific_reports_to_view = Reports.query.filter_by(rack_id = specific_rack_id).order_by(Reports.report_date.desc(), Reports.report_time.desc())
            specific_report_count = specific_reports_to_view.count()
            try:
                flash("You are now viewing reports specifically for bike rack " + str(specific_rack_id) + ".")
                return render_template("specific_reports.html", specific_reports_to_view=specific_reports_to_view,
                                    specific_report_count=specific_report_count, 
                                    specific_rack_id=specific_rack_id)
            except:
                flash("There was an error getting the reports. Please try again later.")
                return redirect(url_for("main_bp.reports_page"))
        else:
            flash("A bike rack with that ID does not exist. You have been returned to the reports page.")
            return redirect(url_for("main_bp.reports_page"))