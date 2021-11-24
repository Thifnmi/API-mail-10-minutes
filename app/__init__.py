from flask import Flask
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .flask_celery import make_celery
from flask_mail import Mail


app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND'] = 'db+sqlite:///database.db'
app.config.from_object('config')


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ""
app.config['MAIL_PASSWORD'] = ""


celery = make_celery(app=app)
db = SQLAlchemy(app)
mail = Mail(app=app)
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
