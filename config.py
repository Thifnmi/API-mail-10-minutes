"""Flask config class."""
import os
import json
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


def _get_config_value(key, default_value=None):
    value = os.environ.get(key, default_value)
    if (value is not None and value != "") and isinstance(value, str):
        if value.isdigit():
            value = int(value)
        elif isinstance(value, str) and key.endswith("LIST"):
            value = json.loads(value)

    return value


class Config(object):
    """Base config vars."""
    SECRET_KEY = _get_config_value("SECRET_KEY", "")

    # Celery configuration
    CELERY_BROKER_URL = _get_config_value("CELERY_BROKER_URL", "")
    CELERY_BACKEND = _get_config_value("CELERY_BACKEND", "")

    SQLALCHEMY_DATABASE_URI = _get_config_value("SQLALCHEMY_DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'thifnmi.pw'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "systemail10p@thifnmi.pw"
    # "MAIL_PASSWORD": 'qfdyskfuokajpxas'


class DevConfig(Config):
    DEBUG = True


app_config = {
    'dev': Config,
}
