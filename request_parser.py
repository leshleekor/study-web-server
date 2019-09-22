class RequestParser:
  def __init__(self, f):
    self.message_header = {}

    message = f.readline().decode("utf-8");
    requestlines = message.split(" ");

    self.method = requestlines[0]
    self.request_uri = requestlines[1]
    self.http_version = requestlines[2]

    while True:
      message = f.readline().decode("iso-8859-1")
      if message == '\r\n':
        break

      messages = message.split(":")
      self.message_header[messages[0]] = messages[1].rstrip('\r\n').strip()

    # self.message_body = f.read(
    #   int(self.message_header["Content-Length"])
    # ).decode("utf-8")
