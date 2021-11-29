from app import app
import sys
from threading import Thread
# import app.dashboard.smtp_server as a
from app import run_smtp

# Thread(target=a.CustomSMTPServer, args=(('192.168.66.177', 1025), None)).start()
Thread(target=run_smtp, args=(1025, )).start()

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    # Thread(target=CustomSMTPServer, args=(('192.168.66.177', 2525), None)).start()
    app.run(debug=True, host='0.0.0.0', port=port)