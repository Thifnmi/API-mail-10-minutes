from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import Config, app_config
from flask_migrate import Migrate
# from .flask_celery import make_celery
# from celery import Celery


# celery = make_celery()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
limit = Limiter(
    key_func=get_remote_address,
    default_limits=['500/day', '200/hour', '20/minute']
)


def create_app(config_name, register_blueprints=True):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    # app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    limit.init_app(app)
    # celery.init_app(app)

    if register_blueprints:
        app = register_blueprint(app)
    # return app
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/auth")
    # from app.api import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix="/api")
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)
    return app


def register_blueprint(app):
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    return app



from app import models
