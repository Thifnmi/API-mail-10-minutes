from flask import request, make_response
from app.models import UserMail, MailBox
from app.base import get_current_time, get_ipv4, convert_to_time
import string
import random
import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.api import bp


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


@bp.route('/', methods=['GET'])
def generator_follow_ip():
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


@bp.route('/generator', methods=['GET'])
def generator_follow_cookie(char_num=4, num=5):
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