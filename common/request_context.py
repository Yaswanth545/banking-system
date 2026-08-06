import threading

_local = threading.local()


def set_request_id(request_id):
    _local.request_id = request_id


def get_request_id():
    return getattr(_local, "request_id", None)