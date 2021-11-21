from app import db
from sqlalchemy.exc import SQLAlchemyError


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)

    def __init__(self, name, password, admin):
        self.name = name
        self.password = password
        self.admin = admin


class UserMail(db.Model):
    __tablename__ = 'usermail'
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    ipv4_ad = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, cookie, email, ipv4_ad, time):
        self.cookie = cookie
        self.email = email
        self.ipv4_ad = ipv4_ad
        self.time = time

    def __repr__(self):
        return '["id": "{}", "email": "{}"]'.format(self.id, self.email)


class MailBox(db.Model):
    __tablename__ = 'mailbox'
    id = db.Column(db.Integer, primary_key=True)
    mail_id = db.Column(db.Integer, db.ForeignKey(
        'usermail.id'), nullable=False)
    mail = db.relationship(
        'UserMail', backref=db.backref('MailBox', lazy=True))
    email_from = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, mail_id, email_from, title, content):
        self.mail_id = mail_id
        self.email_from = email_from
        self.title = title
        self.content = content

    def __repr__(self):
        return '["from": "{}", "title": "{}", "content": "{}"]'.format(
            self.email_from, self.title, self.content)
