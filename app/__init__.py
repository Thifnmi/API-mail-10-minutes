from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import app_config
from flask_migrate import Migrate
# from app.smtp_server.server import SMTPServer
import socket, errno


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
    app.config.from_pyfile('/home/thifnmi/Desktop/VCC_cau8/config.py')

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    limit.init_app(app)
    checkport()

    if register_blueprints:
        app = register_blueprint(app)
    return app


def register_blueprint(app):
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    return app


def checkport():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('0.0.0.0', 1025))
    except:
        from app.smtp_server import bp
    sock.close()


from app.models import models
