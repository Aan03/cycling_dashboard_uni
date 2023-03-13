from flask import Blueprint, render_template
from main_flask_app.dash_app_cycling import *
main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@main_bp.route("/reports")
def reports():
    return render_template("reports.html")