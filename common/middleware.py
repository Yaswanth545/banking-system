import uuid
import logging
import time

from common.request_context import set_request_id



logger = logging.getLogger(__name__)


class RequestIDMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request_id = str(uuid.uuid4())[:8]

        set_request_id(request_id)

        request.request_id = request_id

        start_time = time.perf_counter()

        response = self.get_response(request)

        execution_time = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "%s %s %s %.2f ms",
            request.method,
            request.path,
            response.status_code,
            execution_time,
        )

        response["X-Request-ID"] = request_id

        return response