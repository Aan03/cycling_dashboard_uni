from flask import current_app as app, jsonify, make_response, request
from sqlalchemy import func, desc
from main_flask_app import db, db_session
from main_flask_app.models import Reports, boroughs_list, cycle_parking_data
from main_flask_app.schemas import reports_schema

@app.route("/api/reports", methods=["GET"])
def get_all_reports():
    if request.method == "GET":
        all_reports = db.session.execute(db.select(Reports).order_by(desc(Reports.report_date), 
                                                                    desc(Reports.report_time))).scalars()
        reports_dump = reports_schema.dump(all_reports)
        response_json = jsonify({"report":reports_dump})
        response_json.headers["Content-Type"] = "application/json"
        return make_response(response_json, 200)

boroughs = []
for x in db_session.query(boroughs_list.borough):
    boroughs.append(list(x))
boroughs = [element for nestedlist in boroughs for element in nestedlist]
boroughs.remove("All Boroughs")
boroughs_lower = []
for i in boroughs:
    boroughs_lower.append(i.lower())

@app.route("/api/reports/borough/<borough>", methods=["GET"])
def get_borough_reports(borough):
    if request.method == "GET":
        if borough in boroughs_lower:
            borough_reports = db.session.execute(db.select(Reports).filter(func.lower(Reports.report_borough)
                    ==borough.lower()).order_by(desc(Reports.report_date), desc(Reports.report_time))).scalars()
            reports_dump = reports_schema.dump(borough_reports)
            response_json = jsonify({"report":reports_dump})
            response_json.headers["Content-Type"] = "application/json"
            return make_response(response_json, 200)
        else:
            return make_response("404: The borough name is incorrect or it does not exist.", 404)

rack_id_list = []
for x in db_session.query(cycle_parking_data.feature_id):
    rack_id_list.append(list(x))
rack_id_list = [element for nestedlist in rack_id_list for element in nestedlist]
rack_id_list_lower = []
for i in rack_id_list:
    rack_id_list_lower.append(i.lower())

@app.route("/api/reports/rack/<report_rack_id>", methods=["GET"])
def get_rack_id_reports(report_rack_id):
    if request.method == "GET":
        if str(report_rack_id) in rack_id_list_lower:
            rack_id_reports = db.session.execute(db.select(Reports).filter((Reports.rack_id)== 
                                str(report_rack_id.upper())).order_by(desc(Reports.report_date), desc(Reports.report_time))).scalars()
            reports_dump = reports_schema.dump(rack_id_reports)
            response_json = jsonify({"report":reports_dump})
            return make_response(response_json, 200)
        else:
            return make_response("404: The bike rack ID is incorrect or it does not exist.", 404)