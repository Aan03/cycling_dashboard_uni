from main_flask_app import ma
from main_flask_app.models import Reports


class ReportsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reports
        include_fk = True


reports_schema = ReportsSchema(many=True)
