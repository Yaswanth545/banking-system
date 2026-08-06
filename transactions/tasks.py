from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)



User = get_user_model()


@shared_task
def send_welcome_email(user_id):

    logger.info(
        "Welcome email task started | UserID=%s",
        user_id,
    )

    user = User.objects.get(id=user_id)

    send_mail(
        subject="Welcome to ABC Bank",
        message=(
            f"Hello {user.username},\n\n"
            "Welcome to ABC Bank.\n"
            "Your account has been created successfully."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    logger.info(
        "Welcome email sent | Email=%s",
        user.email,
    )

    return "Email Sent"