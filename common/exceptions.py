from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from .business_exceptions import BusinessException




def custom_exception_handler(exc, context):
    """
    Custom exception handler for all DRF exceptions.
    """

    response = exception_handler(exc, context)

    if isinstance(exc, BusinessException):
        return Response(
            {
                "success": False,
                "message": exc.message,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {
            "success": False,
            "message": "Validation failed.",
            "errors": response.data,
        },
        status=response.status_code,
    )

