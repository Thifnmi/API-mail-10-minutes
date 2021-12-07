from flask import jsonify, request
from werkzeug.security import generate_password_hash
from app.auth.routes import token_required
from app.models.models import UserMail, MailBox, Account
from app import db
from sqlalchemy.exc import SQLAlchemyError
from app.api import bp
from app.utils.base import get_current_time, convert_to_time


@bp.route("/manager", methods=["GET"])
@token_required
def manager(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    if UserMail.query.count() is not None:
        mails = UserMail.query.all()
        res = []
        for mail in mails:
            mail_data = {}
            mail_data['id'] = mail.id
            mail_data['cookie'] = mail.cookie
            mail_data['email'] = mail.email
            mail_data['ipv4_ad'] = mail.ipv4_ad
            mail_data['created_on'] = mail.time
            res.append(mail_data)

        return jsonify({"Email": res}), 200

    return jsonify({'message': "Database empty"}), 200


@bp.route('/create-user', methods=['POST'])
@token_required
def create_user(current_acc):
    if not current_acc.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    if Account.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'This name already exist'})

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_acc = Account(name=data['name'], password=hashed_password, admin=False)
    try:
        db.session.add(new_acc)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'message': 'Create user error'}), 400


@bp.route('/delete-email', methods=['POST'])
@token_required
def delete_mail(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    if UserMail.query.filter_by(id=id).first():
        mail = UserMail.query.filter_by(id=id).first()
        mail_detail = MailBox.query.filter_by(mail_id=id).all()
        try:
            db.session.delete(mail)
            for email_del in mail_detail:
                db.session.delete(email_del)
            db.session.commit()
            return jsonify({"message": "Delete succesful"}), 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message": "Delete error"}), 400

    return jsonify({"message": "Email not exist"}), 404


@bp.route("/check-expiration-email", methods=["POST"])
@token_required
def check_expiration_email(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403
    all_email = UserMail.query.all()
    res = {}
    no = 0
    for email in all_email:
        now = get_current_time()
        if now.timestamp() - convert_to_time(email.time).timestamp() > 30*60:
            mails_comming = MailBox.query.filter_by(mail_id=email.id).all()
            try:
                db.session.delete(email)
                no += 1
                for mail in mails_comming:
                    db.session.delete(mail)
                db.session.commit()
                res['message'] = "Deleted"
            except SQLAlchemyError:
                db.session.rollback()
                res['message'] = "Error, rollback database"
        if no == 0:
            res['message'] = "No expiration email"
    return jsonify({'response': res})
