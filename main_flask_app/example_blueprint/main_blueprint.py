from flask import Blueprint, render_template
example_blueprint = Blueprint('example_blueprint', __name__, template_folder = "templates", static_folder="static")

#@example_blueprint.route('/')
#def index():
#    return "test"

@example_blueprint.route("/")
def index():
    return render_template("index.html")

@example_blueprint.route("/dashboard/")
def indexdash():
    return render_template("dashboard.html")

