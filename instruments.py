import os
from dotenv import load_dotenv
import sentry_sdk

# Загружаем переменные из .env
load_dotenv()

def sentry_init():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Enable sending logs to Sentry
        enable_logs=True,
)