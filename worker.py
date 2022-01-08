import os
import click
from app import consumer


@click.command()
@click.option(
    '--mode', default='celery',
    help="You have two options 'celery' or 'kafka'. celery is defeaul value")
def worker(mode):
    """Try 'python/python3 worker.py --help' for help"""
    if mode == "kafka":
        print('run kafka consumer')
        consumer()
    else:
        print('run celery')
        os.system('celery -A flask_celery:celery worker --loglevel=info')


if __name__ == "__main__":
    worker()
