from flask import request, jsonify
from app.models.models import MailBox
from app.api import bp
from app import limit


@bp.route("/mailbox", methods=["GET"])
@limit.limit('1000/second')
def mailbox():
    if request.args.get('mail_id'):
        mail_id = request.args.get('mail_id')
        if MailBox.query.filter_by(mail_id=mail_id).all():
            results = MailBox.query.filter_by(mail_id=mail_id).all()
            response = []
            for result in results:
                res = {}
                res['mailbox_id'] = result.id
                res['from'] = result.email_from
                res['title'] = result.title
                res['content'] = result.content
                response.append(res)
            return jsonify({'info': response})

        return jsonify({'message': 'mail_id not exist or deleted'}), 400

    return jsonify({'message': "try with '/mailbox?mail_id=<mail_id>'"}), 404


@bp.route("/mailbox/<id>", methods=["GET"])
@limit.limit('1000/second')
def maildetail(id):
    if MailBox.query.filter_by(id=id).all():
        result = MailBox.query.filter_by(id=id).first()
        res = {}
        res['email_id'] = result.id
        res['from'] = result.email_from
        res['title'] = result.title
        res['content'] = result.content
        return jsonify({'info': res})

    return jsonify({'message': 'Email not exist'})
