from flask import current_app as app, jsonify, make_response, request
from sqlalchemy import func, desc
from passlib.hash import sha256_crypt
from main_flask_app import db, db_session
from main_flask_app.models import Reports, boroughs_list, cycle_parking_data, Users
from main_flask_app.schemas import reports_schema
from datetime import datetime
current_date = datetime.today().strftime('%Y-%m-%d')
current_time = datetime.today().strftime('%H:%M')

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


rack_id_query = db_session.query(cycle_parking_data.feature_id)
rack_id_list = []
for x in rack_id_query:
    rack_id_list.append(x[0])
each_rack_borough_query = db_session.query(cycle_parking_data.borough)
each_rack_borough_list = []
for x in each_rack_borough_query:
    each_rack_borough_list.append(x[0])

@app.route("/api/reports/create", methods=["POST"])
def post_report():
    new_report = {"username" : request.json["username"],
                  "password" : request.json["password"],
                  "rack_id" : request.json["rack_id"],
                  "details" : request.json["details"]
                  }
    
    post_username = (new_report["username"]).lower()
    post_password = new_report["password"]
    post_rack_id = new_report["rack_id"]
    post_details = new_report["details"]
    
    user_check = Users.query.filter_by(username=post_username).first()
    if user_check:
        if sha256_crypt.verify(post_password, user_check.password) == True:
            if post_rack_id in rack_id_list:
                index = rack_id_list.index(post_rack_id)
                new_report = Reports(reporter_id=user_check.id,
                             report_borough=each_rack_borough_list[index],
                             rack_id=post_rack_id, 
                             report_date=current_date, 
                             report_time=current_time, 
                             report_details=post_details)
                db.session.add(new_report)
                db.session.commit()
                return jsonify("Theft report added successfully.")
            else:
                return jsonify('A bike rack with that ID was not found.')
        else:
            return jsonify('Password recieved was incorrect.')
    else:
        return jsonify("A user with the username " + new_report["username"] + " does not exist.")
    
    
    
    

    
       
'''
@app.route("/api/reports/delete/<id>", methods=["DELETE"])
def report_delete(id):
    guide = Guide.query.get(id)
    db.session.delete(guide)
    db.session.commit()

    return "Guide was successfully deleted"'''