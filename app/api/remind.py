from flask import request, jsonify
from app.api import bp
import smtplib
from app import limit


@bp.route('/notify', methods=['POST'])
@limit.limit('1000/second')
def notify():
    data = request.get_json()
    try:
        msg = data['message']
        time = data['time']
        email = data['email']
        res = {}
        res['msg'] = msg
        res['email'] = email
        res['time notify'] = time
        client = smtplib.SMTP('192.168.66.177', 1025)
        client.set_debuglevel(True)
        try:
            client.sendmail('sysmail10p@thifnmi.pw', email, msg)
        finally:
            client.quit()
        return jsonify({"Set notify succesful": res}), 201
    except (TypeError, KeyError) as e:
        return jsonify({"Set error": e}), 400
