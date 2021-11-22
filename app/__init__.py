from flask import Flask
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .dashboard.flask_celery import make_celery


app = Flask(__name__)


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND'] = 'db+sqlite:///database.db'
app.config.from_object('config')


# Flask-Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'


celery = make_celery(app=app)
db = SQLAlchemy(app)
limit = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['500/day', '200/hour', '20/minute']
)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': "URL not found"}), 404


from app.dashboard.controller import blueprint


app.register_blueprint(blueprint)
# db.create_all()
