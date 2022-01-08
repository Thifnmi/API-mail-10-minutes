"""Flask config class."""
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Base config vars."""
    SECRET_KEY = "f0e1e037be55b9926d51d2dc20481b46"

    # Celery configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_BACKEND = 'redis://localhost:6379/0'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@10.29.0.6:3306/taotenladb'
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
