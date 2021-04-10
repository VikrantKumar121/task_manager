from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@task(name="send_mail_task")
def send_mail_task( actor_name, recipient_list ):
    """sends an mail when a new task is created successfully"""

    subject = 'New Task'
    message = f'Hi {actor_name}, You have been assigned a new task'
    email_from = settings.EMAIL_HOST_USER
    logger.info("Sent task email")
    return send_mail( subject, message, email_from, recipient_list )
