from main_flask_app import db
from main_flask_app.models import Reports
from main_flask_app.schemas import ReportsSchema


# Marshmallow Schemas
Reports_schema = ReportsSchema(many=True)
Reports_schema = ReportsSchema()


def get_reports():
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_Reports = db.session.execute(db.select(Reports)).scalars()
    reports_json = Reports_schema.dump(all_Reports)
    return reports_json

"""
<form method="post" action="{{ url_for('filter_by_borough') }}">
  <p>Borough Selection:</p>
  <select name="borough_select" id="borough_select">
    {% for borough in boroughs %}
        <option value="{{borough}}">{{borough}}</option>
    {% endfor %}
  </select>
  <button type="submit">Filter</button>
</form>
-->
"""