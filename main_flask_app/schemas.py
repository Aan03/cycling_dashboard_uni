from main_flask_app import ma
from marshmallow import Schema, fields

class ReportsSchema(ma.Schema):
    fields = ("email", "date_created", "_links")
""" Marshmallow schema defining the attributes for creating reports."""