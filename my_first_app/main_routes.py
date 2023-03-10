from flask import render_template, Blueprint, abort

# Define the Blueprint
main_bp = Blueprint("main", __name__, template_folder = "templates")

@main_bp.errorhandler(500)
def internal_server_error(e):
    """Custom error message for Internal Server Error status code 500"""
    return render_template("500.html"), 500

@main_bp.errorhandler(404)
def page_not_found(e):
    """Custom error message for Not Found error with status code 404"""
    return render_template("404.html"), 404

@main_bp.route("/")
def index():
    """Returns the home page"""
    return render_template("templates/index.html")
'''
@main_bp.route("/display_event/<event_id>")
def display_event(event_id):
    """Returns the event detail page"""
    ev = get_event(event_id)
    if ev:
        return render_template("event.html", event=ev)
    else:
        abort(404)
'''