import os

from dotenv import load_dotenv  # Импортируем dotenv
from flask import (
    Flask,
)
from flask_cors import CORS

from app.handlers import handlers
from app.instruments import sentry_init

sentry_init()

load_dotenv()  # Загрузка переменных окружения из файла .env

# Это callable WSGI-приложение
app = Flask(__name__)
app.logger.setLevel("INFO")

if os.getenv("APP_ENV") == "development":
    CORS(
        app,
        origins=["http://localhost:5173"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
        expose_headers=["Content-Range", "Accept-Ranges"],
      )

handlers(app)


@app.errorhandler(404)
def not_found(error):
    return {"detail": "Resource is not found"}, 404

# uv run flask --app app.main run --port 8080  - запуск development сервера