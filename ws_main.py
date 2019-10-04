# webapp 불러오기
from webapp.app import app

from cgi import run_with_cgi

from socket import *
import threading
from threader import request_thread

def main(host="127.0.0.1", port=8080):
    socks = []
    with socket() as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(6)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(
                target=request_thread,
                args=(conn, addr, host, port)
            )
            thread.start()


if __name__ == '__main__':
    main()


