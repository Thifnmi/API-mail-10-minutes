from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import generator_mail, mailbox, manager, remind, send_email
