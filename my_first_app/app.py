from flask import Flask, render_template


app = Flask(__name__, template_folder = 'templates')
#app.config.from_object(Config)

@app.route('/')
def hello_world():
   # return 'Hello World!'
    return render_template("templates.index.html")
    #return app.config['SECRET_KEY']

if __name__ == '__main__':
    app.run(debug=True)