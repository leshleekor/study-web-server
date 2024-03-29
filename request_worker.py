from validation_header import *
from cgi import run_with_cgi
from webapp.app import app

class RequestWorker:

    # DATA
    # self.f
    # self.write_f
    # self.request_line
    # self.header

    def __init__(self, conn, addr, host, port):
        self.host = host
        self.port = port
        self.conn = conn

        self.f = self.conn.makefile('rb')
        self.write_f = self.conn.makefile('wb')

        self.parse_request_line()
        self.parse_header()

        for key, value in self.header.items():
            print(key, value)
            response = self.validation_header(key, value)
            if response is not True:
                self.write_f.write(bytes('HTTP/1.1 %s\r\n' % '400', 'utf-8'))
                self.write_f.write(bytes('400 BAD REQUEST', 'utf-8'))
                self.write_f.flush()
                self.conn.close()

        self.read_body()


    def parse_request_line(self):
        # RFC 2616 - 5.1. Request-Line
        message = self.f.readline().decode("utf-8")
        message = message.split(" ")

        self.request_line = {
            "method": message[0],
            "uri": message[1],
            "version": message[2].rstrip()
        }


    def parse_header(self):
        # RFC 2616 - 4.5., 5.3., 7.1. Header
        self.header = {}
        while True:
            message = self.f.readline().decode("iso-8859-1")
            if message == '\r\n':
                break

            message = message.split(":")
            self.header[message[0]] = message[1].rstrip('\r\n').strip()


    def validation_header(self, key, value):
        # RFC 2616 - 6.1. Status-Line
        return {
            'Host': check_host,
            'Cache-Control': check_cache_control,
            'Connection': check_connection,
            'Content-Length': check_content_length
        }.get(key, default)(value)


    def read_body(self):
        run_with_cgi(
            app,
            self.host,
            self.port,
            self.request_line,
            self.header,
            self.f,
            self.write_f,
        )
        self.conn.close()
