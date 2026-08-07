from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "go to the /ping"


@app.route('/ping')
def ping():
    return "pong"

@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404