from flask import Blueprint, render_template
from multi_page_app import *
example_blueprint = Blueprint('example_blueprint', __name__, template_folder = "templates", static_folder="static")

#@example_blueprint.route('/')
#def index():
#    return "test"

@example_blueprint.route("/")
def index():
    return render_template("index.html")


