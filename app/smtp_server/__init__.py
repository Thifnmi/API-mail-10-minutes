from flask import Blueprint

bp = Blueprint('smtp_server', __name__)

from app.smtp_server import server