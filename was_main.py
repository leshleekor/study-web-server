# webapp 불러오기
from webapp.app import app

from request_parser import RequestParser
from run_cgi import run_with_cgi

from socket import *
import threading

def main(host="127.0.0.1", port=8080):
  socks = []
  with socket() as s:
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(6)


    while True:
      conn, addr = s.accept()
      f = conn.makefile('rb')
      wf = conn.makefile('wb')
      # rp = RequestParser(f)

      message_header = {}
      message = f.readline().decode("utf-8")
      requestlines = message.split(" ")
      method = requestlines[0]
      request_uri = requestlines[1]
      http_version = requestlines[2]

      while True:
        message = f.readline().decode("iso-8859-1")
        if message == '\r\n':
          break

        messages = message.split(":")
        message_header[messages[0]] = messages[1].rstrip('\r\n').strip()

      run_cgi = threading.Thread(target=run_with_cgi, \
        args=(app, host, port, method, request_uri, http_version, \
        message_header, f, wf))
      run_cgi.start()


if __name__ == '__main__':
    main()


