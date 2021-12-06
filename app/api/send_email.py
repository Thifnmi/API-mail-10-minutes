from app.base import get_ipv4
from flask import request, jsonify
from app.models import MailBox, UserMail
from extentions import celery
import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.api import bp


@bp.route('/sendmail', methods=['POST'])
def call_sendmail():
    ipv4_ad = get_ipv4()
    email_from = None
    email_to = None
    title = None
    content = None
    if request.cookies.get('cookies'):
        cookie = request.cookies.get('cookies')
        email_from = UserMail.query.filter_by(cookie=cookie).first().email
        data = request.get_json()
        if data['email_to'] and data['subject'] and data['mail_content']:
            email_to = data['email_to']
            title = data['subject']
            content = data['mail_content']
    else:
        cookie = None
    print("midle")
    result = sendmail.delay(ipv4_ad, cookie, email_from,
                            email_to, title, content)
    res = {}
    res['id'] = result.id
    res['result'] = result.get()
    return jsonify({'message': res})


@celery.task()
def sendmail(ipv4_ad, cookie, email_from, email_to, title, content):
    print("123")
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=7)))
    if cookie is not None:
        if email_to is not None:
            if UserMail.query.filter_by(email=email_to).first():
                mail_id = UserMail.query.filter_by(email=email_to).first().id
                if UserMail.query.filter_by(
                    cookie=cookie, ipv4_ad=ipv4_ad).first() and (
                        now.timestamp() - datetime.datetime.strptime(
                            (UserMail.query.filter_by(cookie=cookie).order_by(
                                UserMail.id.desc()).first()).time,
                            "%Y-%m-%d %H:%M:%S").timestamp() < 600):
                    if email_from and title and content is not None:
                        message = MailBox(
                            mail_id=mail_id, email_from=email_from,
                            title=title, content=content)
                        try:
                            db.session.add(message)
                            db.session.commit()
                            res = "email has been sent"
                        except SQLAlchemyError:
                            db.session.rollback()
                            res = "insert error, rollback database"
                    else:
                        res = "missing data"
                else:
                    res = "Invalid cookie"
            else:
                res = "Email not exist"
        else:
            res = "Missing email_to"
    else:
        res = "Missing cookie"
    return res
