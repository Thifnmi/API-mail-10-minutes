from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import string
import random
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0e1e037be55b9926d51d2dc20481b46'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
limit = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['500/day', '200/hour', '20/minute']
)


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)


class UserMail(db.Model):
    __tablename__ = 'usermail'
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    ipv4_ad = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(120), nullable=False)

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

    def __repr__(self):
        return '["from": "{}", "title": "{}", "content": "{}"]'.format(
            self.email_from, self.title, self.content)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            current_acc = Account.query.filter_by(
                id=data['id']).first()

        except Exception:
            return jsonify({'message': 'Token is invalid!'})

        return f(current_acc, *args, **kwargs)

    return decorated


def get_ipv4():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
        return ip
    return request.environ['HTTP_X_FORWARDED_FOR']


@app.route("/", methods=['GET'])
@limit.limit('10/minute')
def wellcome():
    ip = get_ipv4()
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=7)))
    if UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first() and (
                now.timestamp() - datetime.datetime.strptime(
                    (UserMail.query.filter_by(ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time, "%Y-%m-%d %H:%M:%S"
                ).timestamp() < 600):
        obj = UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first()
        res = {}
        res['id'] = str(obj.id)
        res['email'] = obj.email
    else:
        provider = ['zwoho', 'couly', 'boofx', 'bizfly', 'vccorp']
        char = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(3))
        nums = ''.join(random.choice(string.digits) for _ in range(5))
        supplier = random.choice(provider)
        email_temp = str(char) + str(nums) + "@" + supplier + ".com"
        cookie = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(20))
        email = UserMail(
            cookie=cookie, email=email_temp, ipv4_ad=ip,
            time=datetime.datetime.now(datetime.timezone(
                datetime.timedelta(hours=7))).strftime(
                "%Y-%m-%d %H:%M:%S"))
        try:
            db.session.add(email)
            db.session.commit()
            obj = UserMail.query.filter_by(
                email=email_temp).first()
            id = obj.id
            message_default(id, email_temp)
            result = {}
            result['id'] = str(id)
            result['email'] = email_temp
            res = make_response(result)
            res.set_cookie('cookies', cookie, max_age=60*10)
        except SQLAlchemyError:
            print(type(SQLAlchemyError))
            db.session.rollback()
            # res = {}
            res['message'] = "Error"
    return res, 200


def message_default(mail_id, mail_temp):
    email_from = "systemmail10p@gmail.com"
    title = "Wellcome to mail 10p system"
    content = f"Your email is {mail_temp}"
    message = MailBox(mail_id=mail_id, email_from=email_from,
                      title=title, content=content)
    try:
        db.session.add(message)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()


@app.route("/generator", methods=['GET'])
@limit.limit("1/5second", override_defaults=False)
def generator(char_num=3, num=5):
    if request.cookies.get('cookies') and\
       UserMail.query.filter_by(cookie=request.cookies.get('cookies')).first():
        obj = UserMail.query.filter_by(
            cookie=request.cookies.get('cookies')).first()
        res = {}
        res['id'] = str(obj.id)
        res['email'] = obj.email
    else:
        ip = get_ipv4()
        provider = ['zwoho', 'couly', 'boofx', 'bizfly', 'vccorp']
        char = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(char_num))
        nums = ''.join(random.choice(string.digits) for _ in range(num))
        supplier = random.choice(provider)
        email_temp = str(char) + str(nums) + "@" + supplier + ".com"
        cookie = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(20))
        email = UserMail(
            cookie=cookie, email=email_temp, ipv4_ad=ip,
            time=datetime.datetime.now(datetime.timezone(
                datetime.timedelta(hours=7))).strftime(
                "%Y-%m-%d %H:%M:%S"))
        try:
            db.session.add(email)
            db.session.commit()
            obj = UserMail.query.filter_by(
                email=email_temp).first()
            id = obj.id
            message_default(id, email_temp)
            result = {}
            result['id'] = str(id)
            result['email'] = email_temp
            res = make_response(result)
            res.set_cookie('cookies', cookie, max_age=60*10)
        except SQLAlchemyError:
            print(type(SQLAlchemyError))
            db.session.rollback()
            res = {}
            res['message'] = "Error"

    return res


@app.route("/mailbox", methods=["GET"])
def mailbox():
    if request.args.get('mail_id'):
        mail_id = request.args.get('mail_id')
        if MailBox.query.filter_by(mail_id=mail_id).all():
            results = MailBox.query.filter_by(mail_id=mail_id).all()
            response = []
            for result in results:
                res = {}
                res['id'] = result.id
                res['from'] = result.email_from
                res['title'] = result.title
                res['content'] = result.content
                response.append(res)
            return jsonify({'info': response})

        return jsonify({'message': 'mail_id not exist or deleted'})

    return jsonify({'message': "try again with '/mailbox?mail_id=<mail_id>'"})


@app.route("/mailbox/<id>", methods=["GET"])
def maildetail(id):
    if MailBox.query.filter_by(id=id).all():
        result = MailBox.query.filter_by(id=id).first()
        res = {}
        res['id'] = result.id
        res['from'] = result.email_from
        res['title'] = result.title
        res['content'] = result.content
        return jsonify({'info': res})

    return jsonify({'message': 'Email not exist'})


@app.route("/manager", methods=["GET"])
@token_required
def manager(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    if UserMail.query.all() is not None:
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

        return jsonify({"Email": res})

    return jsonify({'message': "Database empty"})


@app.route('/manager/login')
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
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': '\
        Basic realm="Login required!"'})


@app.route('/manager/user', methods=['POST'])
@limit.limit('1/30second')
@token_required
def create_user(current_acc):
    if not current_acc.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_acc = Account(name=data['name'], password=hashed_password, admin=False)
    try:
        db.session.add(new_acc)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'message': 'Create user error'}), 400


@app.route("/manager/del-mail/<id>", methods=["DELETE"])
@token_required
def delete_mail(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    if UserMail.query.filter_by(id=id).first():
        mail = UserMail.query.filter_by(id=id).first()
        mail_detail = MailBox.query.filter_by(mail_id=id).all()
        try:
            db.session.delete(mail)
            for email in mail_detail:
                db.session.delete(email)
            db.session.commit()
            return jsonify({"message": "Delete succesful"}), 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message": "Delete error"}), 400

    return jsonify({"message": "Email not exist"}), 404


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    app.run(debug=True, host='0.0.0.0', port=port)
