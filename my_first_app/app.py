from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def hello_world():
    #return 'Hello World!'
    return app.config['SECRET_KEY']

if __name__ == '__main__':
    app.run(debug=True)