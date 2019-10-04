import os, sys

enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

def unicode_to_wsgi(u):
    # Convert an environment variable to a WSGI "bytes-as-unicode" string
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')

def run_with_cgi(
    application,
    host,
    port,
    request_line,
    headers,
    f,
    write_f
):
    environ = {k: unicode_to_wsgi(v) for k,v in os.environ.items()}
    # environ['wsgi.input']        = sys.stdin.buffer
    environ['wsgi.input'] = f
    environ['wsgi.errors']       = sys.stderr
    environ['wsgi.version']      = (1, 0)
    environ['wsgi.multithread']  = True
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True
    environ['PATH_INFO'] = request_line["uri"]
    environ['SERVER_NAME'] = host
    environ['SERVER_PORT'] = str(port)
    environ['REQUEST_METHOD'] = request_line["method"]

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        # out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            write_f.write(wsgi_to_bytes('HTTP/1.1 %s\r\n' % status))
            for header in response_headers:
                write_f.write(wsgi_to_bytes('%s: %s\r\n' % header))
            write_f.write(wsgi_to_bytes('\r\n'))

        write_f.write(data)
        write_f.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here,
        # *after* the headers are set.  That way, if an error
        # occurs, start_response can only be re-called with
        # exc_info set.

        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()
