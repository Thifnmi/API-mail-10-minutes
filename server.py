from app import run_server, run_smtp
from multiprocessing import Process


def run():
    p1 = Process(target=run_server, args=(8080, ))
    p1.daemon = True
    p1.start()
    p2 = Process(target=run_smtp, args=(1025, ))
    p2.daemon = True
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    run()
