from flask import Flask, render_template
from multi_page_app.stats import create_dash_app
from multi_page_app import *
from main_bp.main_bp import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

create_dash_app(app)

if __name__ == '__main__':
    app.run(debug=True)