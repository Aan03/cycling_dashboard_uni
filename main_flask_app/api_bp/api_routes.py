from flask import current_app, jsonify, make_response, request, Blueprint
from sqlalchemy import func, desc
from passlib.hash import sha256_crypt
from main_flask_app import db, db_dataset
from main_flask_app.models import Reports, boroughs_list, cycle_parking_data, Users
from main_flask_app.schemas import reports_schema
from datetime import datetime
current_date = datetime.today().strftime('%Y-%m-%d')
current_time = datetime.today().strftime('%H:%M')

api_bp = Blueprint('api_bp', __name__)

#API GET Routes
##Get all reports
@api_bp.route("/api/reports", methods=["GET"])
def get_all_reports():
    all_reports = db.session.execute(db.select(Reports).order_by(desc(Reports.report_date), 
                                                                desc(Reports.report_time))).scalars()
    reports_dump = reports_schema.dump(all_reports)
    response_json = jsonify({"report":reports_dump})
    response_json.headers["Content-Type"] = "application/json"
    return make_response(response_json, 200)

boroughs = []
for x in db_dataset.query(boroughs_list.borough):
    boroughs.append(list(x))
boroughs = [element for nestedlist in boroughs for element in nestedlist]
boroughs.remove("All Boroughs")
boroughs_lower = []
for i in boroughs:
    boroughs_lower.append(i.lower())

##Get all reports for a borough
@api_bp.route("/api/reports/borough/<borough>", methods=["GET"])
def get_borough_reports(borough):
    if borough.lower() in boroughs_lower:
        borough_reports = db.session.execute(db.select(Reports).filter(func.lower(Reports.report_borough)
                ==borough.lower()).order_by(desc(Reports.report_date), desc(Reports.report_time))).scalars()
        reports_dump = reports_schema.dump(borough_reports)
        response_json = jsonify({"report":reports_dump})
        response_json.headers["Content-Type"] = "application/json"
        return make_response(response_json, 200)
    else:
        return make_response("404: The borough name is incorrect or it does not exist.", 404)

rack_id_list = []
for x in db_dataset.query(cycle_parking_data.feature_id):
    rack_id_list.append(list(x))
rack_id_list = [element for nestedlist in rack_id_list for element in nestedlist]
rack_id_list_lower = []
for i in rack_id_list:
    rack_id_list_lower.append(i.lower())

##Get all reports for a specific bike rack
@api_bp.route("/api/reports/rack/<report_rack_id>", methods=["GET"])
def get_rack_id_reports(report_rack_id):
    if str(report_rack_id.lower()) in rack_id_list_lower:
        rack_id_reports = db.session.execute(db.select(Reports).filter((Reports.rack_id)== 
                            str(report_rack_id.upper())).order_by(desc(Reports.report_date), desc(Reports.report_time))).scalars()
        reports_dump = reports_schema.dump(rack_id_reports)
        response_json = jsonify({"report":reports_dump})
        return make_response(response_json, 200)
    else:
        return make_response(jsonify("404: The bike rack ID is incorrect or it does not exist."), 404)

##Get all reports made by a user
@api_bp.route("/api/reports/user/<username_get>", methods=["GET"])
def get_all_reports_for_user(username_get):
    user_check = Users.query.filter_by(username=username_get).first()
    if user_check:
        all_reports_by_user = Reports.query.filter_by(reporter_id = 
                                user_check.id).order_by(desc(Reports.report_date), desc(Reports.report_time))

        reports_dump = reports_schema.dump(all_reports_by_user)
        response_json = jsonify({"report":reports_dump})
        response_json.headers["Content-Type"] = "application/json"
        return make_response(response_json, 200)
    else:
        response = jsonify("404: A user with the username " + username_get + " does not exist.")
        return make_response(response, 404)

rack_id_query = db_dataset.query(cycle_parking_data.feature_id)
rack_id_list = []
for x in rack_id_query:
    rack_id_list.append(x[0])
each_rack_borough_query = db_dataset.query(cycle_parking_data.borough)
each_rack_borough_list = []
for x in each_rack_borough_query:
    each_rack_borough_list.append(x[0])

#API POST Routes
##Create a new report
@api_bp.route("/api/reports/create", methods=["POST"])
def post_report():
    new_report = {"username" : request.json["username"],
                  "password" : request.json["password"],
                  "rack_id" : request.json["rack_id"],
                  "details" : request.json["details"]}
    
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
                response = jsonify("Theft report added successfully.")
                return make_response(response, 201)
            else:
                response = jsonify('404: A bike rack with that ID was not found.')
                return make_response(response, 404)
        else:
            response = jsonify('Password received was incorrect.')
            return make_response(response, 200)
    else:
        response = jsonify("404: A user with the username " + post_username + " does not exist.")
        return make_response(response, 404)
    
##Adding a new user
@api_bp.route("/api/user/sign_up", methods=["POST"])
def new_user_api():
    new_user_request = {"username" : request.json["username"],
                        "password" : request.json["password"]}
    
    new_user_username = new_user_request["username"]
    new_user_password = new_user_request["password"]

    encrypted_password = sha256_crypt.encrypt(new_user_password)
    user_check = Users.query.filter_by(username=new_user_username).first()
    if user_check:
        response = jsonify("A user with the username " + new_user_username + " already exists.")
        return make_response(response, 200)
    else:
        new_user = Users(username=new_user_username, password=encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        response = jsonify("User " + new_user_username + " has been signed up successfuly.")
        return make_response(response, 201)
    
#API PUT Routes
##Edit an existing report
@api_bp.route("/api/reports/edit/<int:report_id>", methods=["PUT"])
def edit_report_details(report_id):
    put_request = {"username" : request.json["username"],
                  "password" : request.json["password"],
                  "details" : request.json["details"]}
    put_username = (put_request["username"]).lower()
    put_password = put_request["password"]
    put_details = request.json["details"]
    put_report_id = report_id
    user_check = Users.query.filter_by(username=put_username).first()
    if user_check:
        if sha256_crypt.verify(put_password, user_check.password) == True:
            report_check = Reports.query.filter_by(id=put_report_id).first()
            if report_check:
                if  user_check.id == report_check.reporter_id:
                    report_check.report_details = put_details
                    db.session.commit()
                    response = jsonify("Report details successfully edited.")
                    return make_response(response, 200)
                else:
                    response = jsonify("The report with an id of " + str(put_report_id)
                                   + " does exist but under a different username.")
                    return make_response(response, 200)
            else:
                response = jsonify("404: A report with that ID does not exist.")
                return make_response(response, 404)
        else:
            return jsonify('Password received was incorrect.')
    else:
        response = jsonify("404: A user with the username " + put_username + 
                       " does not exist.")
        return make_response(response, 404)

##Change user password
@api_bp.route("/api/user/change_password", methods=["PUT"])
def change_user_password_api():
    change_password_request = {"username" : request.json["username"],
                               "current_password" : request.json["current_password"],
                               "new_password" : request.json["new_password"]}
    put_req_username = (change_password_request["username"]).lower()
    put_req_old_password = change_password_request["current_password"]
    put_req_new_password = change_password_request["new_password"]
    user_check = Users.query.filter_by(username=put_req_username).first()
    if user_check:
        if sha256_crypt.verify(put_req_old_password, user_check.password) == True:
            new_encrypted_password = sha256_crypt.encrypt(put_req_new_password)
            user_check.password = new_encrypted_password
            db.session.commit()
            response = jsonify("Password changed successfully.")
            return make_response(response, 200)
        else:
            response = jsonify('Current password received was incorrect.')
            return make_response(response, 200)
    else:
        response = jsonify("404: A user with the username " + put_req_username + 
                       " does not exist.")
        return make_response(response, 404)

#API DELETE Routes
##Delete an existing report
@api_bp.route("/api/reports/delete/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):

    delete_request = {"username" : request.json["username"],
                      "password" : request.json["password"]}
    
    delete_req_username = (delete_request["username"]).lower()
    delete_req_password = delete_request["password"]
    delete_req_report_id = report_id

    user_check = Users.query.filter_by(username=delete_req_username).first()
    if user_check:
        if sha256_crypt.verify(delete_req_password, user_check.password) == True:
            report_check = Reports.query.filter_by(id=delete_req_report_id).first()
            if report_check:
                if  user_check.id == report_check.reporter_id:
                    Reports.query.filter_by(id=delete_req_report_id).delete()
                    db.session.commit()
                    response = jsonify("Report deleted successfully.")
                    return make_response(response, 200)
                else:
                    response = jsonify("The report with an id of " + str(delete_req_report_id)
                                   + " does exist but under a different username.")
                    return make_response(response, 200)
            else:
                response = jsonify("404: A report with that ID does not exist.")
                return make_response(response, 404)
        else:
            response = jsonify('Password received was incorrect.')
            return make_response(response, 200)
    else:
        response = jsonify("404: A user with the username " + delete_req_username + 
                       " does not exist.")
        return make_response(response, 404)