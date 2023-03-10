from flask import Flask, render_template
from multi_page_app.stats import create_dash_app
from multi_page_app import *
from example_blueprint.main_blueprint import example_blueprint


app = Flask(__name__)
app.register_blueprint(example_blueprint)


create_dash_app(app)


#@app.route('/')
#def hello_world():
#    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)