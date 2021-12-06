from app import create_app

app = create_app('dev', register_blueprints=True)
