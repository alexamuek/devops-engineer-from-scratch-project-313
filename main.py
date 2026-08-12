import logging

from flask import Flask

from instruments import sentry_init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting application...")

sentry_init()
logger.info("✅ Sentry initialized successfully")

app = Flask(__name__)


@app.route('/')
def index():
    return "go to the /ping"


@app.route('/ping')
def ping():
    return "pong"


@app.route("/error")
def hello_world():
    1 / 0  # raises an error
    return "<p>Hello, World!</p>"


@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404