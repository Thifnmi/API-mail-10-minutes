from app import run_server, run_smtp
import sys
from multiprocessing import Process

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 8080
    p1 = Process(target=run_server, args=(port, ))
    p1.daemon = True
    p1.start()
    p2 = Process(target=run_smtp, args=(1025, ))
    p2.daemon = True
    p2.start()
    p1.join()
    p2.join()
