from app.base import get_ipv4, get_current_time, convert_to_time
from flask import request, make_response
from app.models import MailBox, UserMail
import string
import random
from app import db
import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.errors import bp


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


@bp.errorhandler(429)
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
