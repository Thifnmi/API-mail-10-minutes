import json
import datetime
from app.utils.base import get_ipv4
from flask import request, jsonify
from app.models.models import MailBox, UserMail
from flask_celery import celery
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.api import bp
from kafka import KafkaProducer
from app import limit
from time import sleep


bootstrap_servers = ['localhost:9092']


@bp.route('/send-kafka', methods=['POST'])
@limit.limit('100000/second')
def send_kafka():
    ipv4_ad = get_ipv4()
    email_from = None
    if request.cookies.get('cookies'):
        cookie = request.cookies.get('cookies')
        email_from = UserMail.query.filter_by(cookie=cookie).first().email
        data_post = request.get_json()
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers)
        data_post['ipv4_ad'] = ipv4_ad
        data_post['email_from'] = email_from
        data_post['cookie'] = cookie
        producer.send('test-topics', json.dumps(data_post).encode('utf-8'))
        producer.flush()
        return 'done'
    else:
        return 'missing cookies'


@bp.route('/sendmail', methods=['POST'])
@limit.limit('10/second')
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
    result = sendmail.delay(ipv4_ad, cookie, email_from,
                            email_to, title, content)
    task_id = result.task_id
    re = sendmail.AsyncResult(task_id)
    res = {}
    res['_id'] = re.id
    res['result'] = re.get()
    return jsonify({'message': res})


@celery.task()
def sendmail(ipv4_ad, cookie, email_from, email_to, title, content):
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
                            sleep(10)
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


def consumer_sendmail(data):
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=7)))
    if data['cookie'] is not None:
        if data['email_to'] is not None:
            if UserMail.query.filter_by(email=data['email_to']).first():
                mail_id = UserMail.query.filter_by(
                    email=data['email_to']).first().id
                if UserMail.query.filter_by(
                    cookie=data['cookie'],
                    ipv4_ad=data['ipv4_ad']).first() and (
                        now.timestamp() - datetime.datetime.strptime(
                            (UserMail.query.filter_by(
                                cookie=data['cookie']).order_by(
                                UserMail.id.desc()).first()).time,
                            "%Y-%m-%d %H:%M:%S").timestamp() < 600):
                    if data['email_from'] and data['subject'] and data['mail_content'] is not None:
                        message = MailBox(
                            mail_id=mail_id, email_from=data['email_from'],
                            title=data['subject'], content=data['mail_content'])
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
