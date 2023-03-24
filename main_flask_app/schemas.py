from main_flask_app import db, ma
from main_flask_app.models import Users, Reports


class ReportsSchema(ma.SQLAlchemySchema):
    """Marshmallow schema defining the attributes for creating a report."""

    class Meta:
        model = Reports
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    rack_id = ma.auto_field()
    report_borough = ma.auto_field()
    report_date = ma.auto_field()
    report_time = ma.auto_field()
    report_details = ma.auto_field()
