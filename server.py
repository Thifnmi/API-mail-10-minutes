from app import run_server, run_smtp
from multiprocessing import Process


def run(port1, port2):
    p1 = Process(target=run_server, args=(port1, ))
    p1.daemon = True
    p1.start()
    p2 = Process(target=run_smtp, args=(port2, ))
    p2.daemon = True
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    run(8080, 1025)
