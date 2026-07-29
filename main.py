from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "go to the /ping"


@app.route('/ping')
def ping():
    return "pong"