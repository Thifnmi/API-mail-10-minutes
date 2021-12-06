from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import errors, generator_mail, mailbox, manager, remind, send_email
