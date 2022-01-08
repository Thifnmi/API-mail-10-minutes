from celery import Celery
from app import create_app


class CeleryConfig:
    imports = ('app.api.send_email')
    # result_expires = 120
    # accept_content = ['json', 'msgpack', 'yaml']
    # task_serializer = 'json'
    # result_serializer = 'json'
    # timezone = 'Asia/Ho_Chi_Minh'
    # CELERY_enable_utc = False
    # result_backend = 'db+sqlite:///database.db'


def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_BACKEND']
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
