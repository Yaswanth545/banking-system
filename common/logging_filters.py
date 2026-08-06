import logging

from common.request_context import get_request_id


class RequestIDFilter(logging.Filter):
    """
    Adds the request_id to every log record.
    """

    def filter(self, record):
        record.request_id = get_request_id() or "-"
        return True

    