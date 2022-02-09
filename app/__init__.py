from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import app_config
from flask_migrate import Migrate
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
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    limit.init_app(app)
    # checkport()

    if register_blueprints:
        app = register_blueprint(app)
    app.app_context().push()
    return app


def register_blueprint(app):
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth/v1")
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")
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


def consumer():
    import json
    from kafka import KafkaConsumer
    from app.api.send_email import consumer_sendmail

    bootstrap_servers = ['localhost:9092']

    cons = KafkaConsumer(
        'test-topics',
        group_id='group1',
        bootstrap_servers=bootstrap_servers,
        enable_auto_commit=True)

    for message in cons:
        data = json.loads(message.value.decode('utf-8'))
        consumer_sendmail(data=data)


from app.models import models