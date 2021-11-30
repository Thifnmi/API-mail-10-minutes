from app import app
import sys
# from threading import Thread
# from app import run_smtp


# Thread(target=run_smtp, args=(1025, )).start()

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    app.run(debug=True, host='0.0.0.0', port=port)
