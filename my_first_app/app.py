from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__, template_folder = 'templates')
app.config.from_object(config.Config)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)