from flask import Blueprint, render_template
from multi_page_app import *
main_bp = Blueprint('main_bp', __name__, template_folder = "templates", static_folder="static")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dash():
    return render_template("dashboard.html")