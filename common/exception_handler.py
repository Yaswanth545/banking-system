import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from common.business_exceptions import BusinessException


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Global DRF exception handler.
    """

    response = exception_handler(exc, context)

    if isinstance(exc, BusinessException):
        return Response(
            {
                "success": False,
                "message": str(exc),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is not None:
        return response

    logger.exception(
        "Unhandled exception",
        exc_info=exc,
    )

    return Response(
        {
            "success": False,
            "message": "Internal server error.",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )