from flask import request
import datetime


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
