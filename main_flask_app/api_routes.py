import csv
from flask import make_response
from main_flask_app.utilities import get_reports
import json
from flask import (
    render_template,
    request,
    make_response,
    jsonify,
    app
)
from main_flask_app import db
from main_flask_app.models import Users, Reports
from main_flask_app.schemas import ReportsSchema

from main_flask_app.dash_app_cycling import *
import csv, json

import pandas as pd
from main_flask_app import db
from main_flask_app.models import Users, Reports
from io import StringIO
# -------
# Schemas
# -------

reports_schema = ReportsSchema(many=True)
reports_schema = ReportsSchema()
# ------
# Routes
# ------


#download csv file
"""
@app.route("/filter_by_borough", methods=["POST"])
def download_reports():
    #Downloads the details for a given Borough as a CSV file.
    # Extract the selected borough from the form data
    borough = request.form.get("borough_select")
    # Return a 404 code if the region is not found in the database
    reports = db.session.query(Reports).filter_by(report_borough=borough).all()
    reports_json = reports_schema.dump(reports)
    # Convert the JSON data to a CSV string
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(reports_json[0].keys())
    for report in reports_json:
        writer.writerow(report.values())
    # Create a response with the CSV data and appropriate headers
    response = make_response(csv_data.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment; filename={borough}_reports.csv"
    return response

"""