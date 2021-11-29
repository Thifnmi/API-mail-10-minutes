from flask import Flask
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .flask_celery import make_celery
from flask_mail import Mail
from .dashboard.smtp_server import CustomSMTPServer


app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND'] = 'db+mysql://root:@localhost/database'
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/database'


# Flask-Mail configuration
mail_settings = {
    "MAIL_SERVER": 'thifnmi.pw',
    "MAIL_PORT": 1025,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "systemail10p@thifnmi.pw"
    # "MAIL_PASSWORD": 'qfdyskfuokajpxas'
}
CustomSMTPServer(('192.168.66.177', 1025), None)

app.config.update(mail_settings)
mail = Mail(app)

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


# def run_server(port):
#     app.run(debug=True, host='0.0.0.0', port=port)


# def run_smtp(port):
#     server = CustomSMTPServer(('192.168.66.177', port), None)
#     print(server)
# asyncore.loop()
