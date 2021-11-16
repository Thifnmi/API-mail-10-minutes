from flask import Flask
import sys
from flask import request


app = Flask(__name__)


# @app.route("/get_my_ip", methods=["GET"])
# def get_my_ip():
#     return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200


@app.route("/", methods=['GET'])
@app.route('/index', methods=['GET'])
def wellcome():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        # print(request.environ['REMOTE_ADDR'])
    else:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        # print(request.environ['HTTP_X_FORWARDED_FOR'])
    return f"Helluuuu {ip} !!!"


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    app.run(debug=True, port=port)
