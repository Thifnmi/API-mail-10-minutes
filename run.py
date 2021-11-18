from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
import sys
import string
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '["id": "{}", "email": "{}"]'.format(self.id, self.email)


class MailBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'), nullable=False)
    mail = db.relationship('Mail', backref=db.backref('Mailbox', lazy=True))
    email_from = db.Column(db.String(120), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '["from": "{}", "title": "{}", "content": "{}"]'.format(
            self.email_from, self.title, self.content)


db.create_all()


@app.route("/", methods=['GET'])
@app.route('/index', methods=['GET'])
def wellcome():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    else:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    mesage = f"<h1 style='text-align: center;'>Wellcome to BackEnd mail\
         temp 10 minutes developed by Thifnmi.</h1>\
              <h1 style='text-align: center;'>Your ip is: {ip}</h1>"
    return mesage


def message_default(mail_id, mail_temp):
    email_from = "systemmail10p@gmail.com"
    title = "Wellcome to mail 10p system"
    content = f"Your email is {mail_temp}"
    message = MailBox(mail_id=mail_id, email_from=email_from,
                      title=title, content=content)
    db.session.add(message)
    db.session.commit()


@app.route("/generator", methods=['GET'])
def generator(char_num=3, num=5):
    if request.cookies.get('cookies') and\
         Mail.query.filter_by(cookie=request.cookies.get('cookies')).first():
        obj = Mail.query.filter_by(
            cookie=request.cookies.get('cookies')).first()
        res = obj.email + " your id email is: " + str(obj.id)
    else:
        provider = ['zwoho', 'couly', 'boofx', 'bizfly', 'vccorp']
        char = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(char_num))
        nums = ''.join(random.choice(string.digits) for _ in range(num))
        supplier = random.choice(provider)
        email_temp = str(char) + str(nums) + "@" + supplier + ".com"
        cookie = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(10))
        email = Mail(cookie=cookie, email=email_temp)
        db.session.add(email)
        db.session.commit()
        obj = Mail.query.filter_by(
            email=email_temp).first()
        id = obj.id
        message_default(id, email_temp)
        res = make_response(email_temp + " your id email is:" + str(id))
        res.set_cookie('cookies', cookie, max_age=60*10)
    return res


@app.route("/mailbox", methods=["GET"])
def mailbox():
    if request.args.get('mail_id'):
        mail_id = request.args.get('mail_id')
        if MailBox.query.filter_by(mail_id=mail_id).all():
            res = MailBox.query.filter_by(mail_id=mail_id).all()
        else:
            res = "Email not exist"
    else:
        res = "url not found, try with /mailbox?mail_id='your email id'"
    return str(res)


@app.route("/mailbox/<id>", methods=["GET"])
def maildetail(id):
    if MailBox.query.filter_by(id=id).all():
        res = MailBox.query.filter_by(id=id).first()
    else:
        res = "Email not exist"
    return str(res)


@app.route("/manager", methods=["GET"])
def manager():
    if Mail.query.all() is not None:
        res = Mail.query.all()
    else:
        res = "List Email empty"
    return str(res)


@app.route("/manager/del-mail/<id>", methods=["DELETE"])
def delete_mail(id):
    if Mail.query.filter_by(id=id).first():
        print(id)
        mail = Mail.query.filter_by(id=id).first()
        mail_detail = MailBox.query.filter_by(mail_id=id).all()
        db.session.delete(mail)
        for email in mail_detail:
            db.session.delete(email)
        db.session.commit()
        res = "Delete succesful"
    else:
        res = "Email not exist"
    return str(res)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    app.run(debug=True, host='0.0.0.0', port=port)
