import os

import sentry_sdk
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


def sentry_init():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        send_default_pii=True,
        enable_logs=True,
)