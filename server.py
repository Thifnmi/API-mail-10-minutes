from app import create_app


def serve():
    app = create_app('dev', register_blueprints=True)
    app.run(host="0.0.0.0", port=8088)


if __name__ == "__main__":
    serve()