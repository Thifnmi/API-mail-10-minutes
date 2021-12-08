from kafka import KafkaConsumer
from app import db
import datetime
from app.models.models import UserMail, MailBox
from sqlalchemy.exc import SQLAlchemyError
import json


bootstrap_servers = ['localhost:9092']

cons = KafkaConsumer(
    'test-topics',
    group_id='group1',
    bootstrap_servers=bootstrap_servers,
    enable_auto_commit=True)

for message in cons:
    data = json.loads(message.value.decode('utf-8'))
    print(data)


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

