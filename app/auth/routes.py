import datetime
import jwt
from flask import request, jsonify, make_response, current_app
from functools import wraps
from app.auth import bp
from werkzeug.security import check_password_hash
from app.models.models import Account


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 400

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms="HS256")
            current_acc = Account.query.filter_by(
                id=data['id']).first()

        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_acc, *args, **kwargs)

    return decorated


@bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': '\
            Basic realm="Login required!"'})

    account = Account.query.filter_by(name=auth.username).first()

    if not account:
        return make_response('Could not verify', 401, {'WWW-Authenticate': '\
            Basic realm="Login required!"'})

    if check_password_hash(account.password, auth.password):
        token = jwt.encode({'id': account.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': '\
        Basic realm="Login required!"'})
