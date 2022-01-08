from flask import Blueprint

bp = Blueprint('server', __name__)

from app.smtp_server import mail_receive, server