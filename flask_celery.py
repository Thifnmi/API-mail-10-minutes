from celery import Celery
from app import create_app


class CeleryConfig:
    CELERY_IMPORTS = ('app.api.send_email')
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
    CELERY_ENABLE_UTC = False
    CELERY_BROKER_URL = 'amqp://localhost//'
    CELERY_BACKEND = 'rpc://localhost//'
# this is a place for scheduler with celery beat.
# so, you can change 'task' part whatever you want.
    CELERYBEAT_SCHEDULE = {
        "time_scheduler": {
            "task": "proj.tasks.what",
            # set schedule time !
            "schedule": 60.0
        }
    }


def make_celery(app):
    celery = Celery(app.import_name,
                    broker='amqp://localhost//',
                    backend='rpc://localhost//'
                    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    celery.config_from_object(CeleryConfig)
    return celery


app = create_app('dev', register_blueprints=False)
celery = make_celery(app)
