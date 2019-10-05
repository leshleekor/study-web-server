def check_host(message):
  return True


def check_cache_control(message):
    return True


def check_connection(message):
    return True


def check_content_length(message):
    if int(message) < 0:
        return False
    else:
        return True


def check_date(message):
    return True


def default(message):
    return True
