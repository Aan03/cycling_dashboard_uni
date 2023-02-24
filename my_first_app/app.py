from flask import Flask
from config import Config

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'



app.config.from_object(Config)

if __name__ == '__main__':
    app.run(debug=True)