from app import celery
from flask import Blueprint, request, jsonify, make_response
import string
import random
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app import db, limit, app
from app.dashboard.database import Account, UserMail, MailBox
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Message
import smtplib
from email.mime.text import MIMEText


blueprint = Blueprint('dashboard', __name__)


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
                token, app.config['SECRET_KEY'], algorithms="HS256")
            current_acc = Account.query.filter_by(
                id=data['id']).first()

        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_acc, *args, **kwargs)

    return decorated


def get_ipv4():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
        return ip
    return request.environ['HTTP_X_FORWARDED_FOR']


def get_current_time():
    now = datetime.datetime.strptime((datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=7)))).strftime(
            "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    return now


def convert_to_time(obj):
    time = datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
    return time


@blueprint.errorhandler(429)
def ratelimit_handler(e):
    ip = get_ipv4()
    now = get_current_time()
    if request.cookies.get('cookies'):
        if UserMail.query.filter_by(cookie=request.cookies.get(
                'cookies'), ipv4_ad=ip).first() and (
                now.timestamp() - convert_to_time(
                    (UserMail.query.filter_by(cookie=request.cookies.get(
                        'cookies')).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
            obj = UserMail.query.filter_by(
                cookie=request.cookies.get('cookies')).first()
            result = {}
            result['id'] = str(obj.id)
            result['email'] = obj.email
            cookie_life_time = now.timestamp() - convert_to_time((
                UserMail.query.filter_by(ipv4_ad=ip).order_by(
                    UserMail.id.desc()).first()).time).timestamp()
            res = make_response(result)
            res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
        else:
            char = ''.join(random.choice(string.ascii_lowercase)
                           for _ in range(4))
            nums = ''.join(random.choice(string.digits) for _ in range(5))
            email_temp = str(char) + str(nums) + "@thifnmi.pw"
            cookie = ''.join(random.choice(string.ascii_lowercase)
                             for _ in range(20))
            new_email = UserMail(
                cookie=cookie, email=email_temp, ipv4_ad=ip,
                time=datetime.datetime.now(datetime.timezone(
                    datetime.timedelta(hours=7))).strftime(
                    "%Y-%m-%d %H:%M:%S"))
            try:
                db.session.add(new_email)
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
                db.session.rollback()
                res = {}
                res['message'] = "Error"
    else:
        if UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first() and (
                now.timestamp() - convert_to_time((UserMail.query.filter_by(
                    ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
            obj = UserMail.query.filter_by(
                ipv4_ad=ip).order_by(UserMail.id.desc()).first()
            res = {}
            res['id'] = str(obj.id)
            res['email'] = obj.email
            res = make_response(res)
            cookie_life_time = now.timestamp() - convert_to_time((
                UserMail.query.filter_by(ipv4_ad=ip).order_by(
                    UserMail.id.desc()).first()).time).timestamp()
            res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
        else:
            if UserMail.query.filter_by(
                ipv4_ad=ip).order_by(UserMail.id.desc()).first() and (
                now.timestamp() - convert_to_time((UserMail.query.filter_by(
                    ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
                obj = UserMail.query.filter_by(
                    ipv4_ad=ip).order_by(UserMail.id.desc()).first()
                res = {}
                res['id'] = str(obj.id)
                res['email'] = obj.email
                res = make_response(res)
                cookie_life_time = now.timestamp() - convert_to_time((
                    UserMail.query.filter_by(ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time).timestamp()
                res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
            else:
                char = ''.join(random.choice(string.ascii_lowercase)
                               for _ in range(4))
                nums = ''.join(random.choice(string.digits) for _ in range(5))
                email_temp = str(char) + str(nums) + "@thifnmi.pw"
                cookie = ''.join(random.choice(string.ascii_lowercase)
                                 for _ in range(20))
                new_email = UserMail(
                    cookie=cookie, email=email_temp, ipv4_ad=ip,
                    time=datetime.datetime.now(datetime.timezone(
                        datetime.timedelta(hours=7))).strftime(
                        "%Y-%m-%d %H:%M:%S"))
                try:
                    db.session.add(new_email)
                    db.session.commit()
                    obj = UserMail.query.filter_by(
                        email=email_temp).first()
                    id = obj.id
                    message_default(id, email_temp)
                    result = {}
                    result['id'] = str(id)
                    result['email'] = email_temp
                    res = make_response(result)
                    res.set_cookie('cookies', cookie, max_age=600)
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {}
                    res['message'] = "Error"
    return res


@blueprint.route("/", methods=['GET'])
@limit.limit('10/minute')
def wellcome():
    ip = get_ipv4()
    now = get_current_time()
    if UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first() and (
                now.timestamp() - convert_to_time((UserMail.query.filter_by(
                    ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
        obj = UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first()
        res = {}
        res['id'] = str(obj.id)
        res['email'] = obj.email
        res = make_response(res)
        cookie_life_time = now.timestamp() - convert_to_time((
            UserMail.query.filter_by(ipv4_ad=ip).order_by(
                UserMail.id.desc()).first()).time).timestamp()
        res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
    else:
        # provider = ['zwoho', 'couly', 'boofx', 'bizfly', 'vccorp']
        char = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(4))
        nums = ''.join(random.choice(string.digits) for _ in range(5))
        # supplier = random.choice(provider)
        email_temp = str(char) + str(nums) + "@thifnmi.pw"
        cookie = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(20))
        new_email = UserMail(
            cookie=cookie, email=email_temp, ipv4_ad=ip,
            time=datetime.datetime.now(datetime.timezone(
                datetime.timedelta(hours=7))).strftime(
                "%Y-%m-%d %H:%M:%S"))
        try:
            db.session.add(new_email)
            db.session.commit()
            obj = UserMail.query.filter_by(
                email=email_temp).first()
            id = obj.id
            message_default(id, email_temp)
            result = {}
            result['id'] = str(id)
            result['email'] = email_temp
            res = make_response(result)
            res.set_cookie('cookies', cookie, max_age=600)
        except SQLAlchemyError:
            db.session.rollback()
            res = {}
            res['message'] = "Error"
    return res, 200


def message_default(mail_id, mail_temp):
    email_from = "systemmail10p@thifnmi.pw"
    title = "Wellcome to mail 10p system"
    content = f"Your email is {mail_temp}"
    message = MailBox(mail_id=mail_id, email_from=email_from,
                      title=title, content=content)
    try:
        db.session.add(message)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()


@blueprint.route("/generator", methods=['GET'])
@limit.limit("1/5second", override_defaults=False)
def generator(char_num=4, num=5):
    ip = get_ipv4()
    now = get_current_time()
    if request.cookies.get('cookies'):
        if UserMail.query.filter_by(cookie=request.cookies.get(
                'cookies'), ipv4_ad=ip).first() and (
                now.timestamp() - convert_to_time(
                    (UserMail.query.filter_by(cookie=request.cookies.get(
                        'cookies')).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
            obj = UserMail.query.filter_by(
                cookie=request.cookies.get('cookies')).first()
            result = {}
            result['id'] = str(obj.id)
            result['email'] = obj.email
            cookie_life_time = now.timestamp() - convert_to_time((
                UserMail.query.filter_by(ipv4_ad=ip).order_by(
                    UserMail.id.desc()).first()).time).timestamp()
            res = make_response(result)
            res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
        else:
            res = {}
            res['message'] = "Invalid cookie"
    else:
        if UserMail.query.filter_by(
            ipv4_ad=ip).order_by(UserMail.id.desc()).first() and (
                now.timestamp() - convert_to_time((UserMail.query.filter_by(
                    ipv4_ad=ip).order_by(
                        UserMail.id.desc()).first()).time).timestamp() < 600):
            obj = UserMail.query.filter_by(
                ipv4_ad=ip).order_by(UserMail.id.desc()).first()
            res = {}
            res['id'] = str(obj.id)
            res['email'] = obj.email
            res = make_response(res)
            cookie_life_time = now.timestamp() - convert_to_time((
                UserMail.query.filter_by(ipv4_ad=ip).order_by(
                    UserMail.id.desc()).first()).time).timestamp()
            res.set_cookie('cookies', obj.cookie, max_age=cookie_life_time)
        else:

            # provider = ['zwoho', 'couly', 'boofx', 'bizfly', 'vccorp']
            char = ''.join(random.choice(string.ascii_lowercase)
                           for _ in range(char_num))
            nums = ''.join(random.choice(string.digits) for _ in range(num))
            # supplier = random.choice(provider)
            email_temp = str(char) + str(nums) + "@thifnmi.pw"
            cookie = ''.join(random.choice(string.ascii_lowercase)
                             for _ in range(20))
            new_email = UserMail(
                cookie=cookie, email=email_temp, ipv4_ad=ip,
                time=datetime.datetime.now(datetime.timezone(
                    datetime.timedelta(hours=7))).strftime(
                    "%Y-%m-%d %H:%M:%S"))
            try:
                db.session.add(new_email)
                db.session.commit()
                obj = UserMail.query.filter_by(
                    email=email_temp).first()
                id = obj.id
                message_default(id, email_temp)
                result = {}
                result['id'] = str(id)
                result['email'] = email_temp
                res = make_response(result)
                res.set_cookie('cookies', cookie, max_age=600)
            except SQLAlchemyError:
                db.session.rollback()
                res = {}
                res['message'] = "Error"

    return res


@blueprint.route("/mailbox", methods=["GET"])
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


@blueprint.route("/mailbox/<id>", methods=["GET"])
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


@blueprint.route('/notify', methods=['POST'])
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


@blueprint.route("/check-expiration-email", methods=["POST"])
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


def send():
    data = request.get_json()
    try:
        subject = data['subject']
        content = data['content']
        sender = data['sender']
        recip = data['recipents']
        for recipient in recip.values():
            msg = MIMEText('This is the body of the message.')
            msg['Subject'] = subject
            msg['Content'] = content
            client = smtplib.SMTP('192.168.66.177', 2525)
            client.set_debuglevel(True)
            try:
                client.sendmail(sender, recipient, msg.as_string())
            finally:
                client.quit()
            res = {}
            res['Message'] = "Done"

    except KeyError as e:
        res = {}
        res['Missing'] = str(e)
    return res


@blueprint.route("/sendmailsmtp", methods=['POST'])
def send_mail_smtp():
    data = request.get_json()
    try:
        subject = data['subject']
        content = data['content']
        sender = data['sender']
        recip = data['recipents']
        recipents = []
        for i in recip.values():
            recipents.append(i)

        from app import mail
        with app.app_context():
            msg = Message(subject=subject, sender=sender,
                          recipients=recipents, body=content)
            mail.send(msg)
            res = "Done"

    except KeyError as e:
        res = {}
        res['Missing'] = str(e)

    return jsonify({"message": res})


@blueprint.route('/sendmail', methods=['POST'])
def call_sendmail():
    ipv4_ad = get_ipv4()
    email_from = None
    email_to = None
    title = None
    content = None
    if request.cookies.get('cookies'):
        cookie = request.cookies.get('cookies')
        email_from = UserMail.query.filter(cookie=cookie).first().email
        data = request.get_json()
        if data['email_to'] and data['subject'] and data['mail_content']:
            email_to = data['email_to']
            title = data['subject']
            content = data['mail_content']
    else:
        cookie = None

    result = sendmail.delay(ipv4_ad, cookie, email_from,
                            email_to, title, content)
    res = {}
    res['id'] = result.id
    res['result'] = result.get()
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
                                UserMail.id.desc()).first()).time, "%Y-%m-%d %H:%M:%S"
                        ).timestamp() < 600):
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


@blueprint.route("/manager", methods=["GET"])
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


@blueprint.route('/manager/login', methods=['GET'])
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


@blueprint.route('/manager/user', methods=['POST'])
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


@blueprint.route("/manager/del-mail/<id>", methods=["DELETE"])
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
