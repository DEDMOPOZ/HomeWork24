from celery import shared_task

from .log_services import delete_old_logs
from .notify_services import email_send, mailing


@shared_task
def send_email(email_to, author):
    email_send(email_to, author)


@shared_task
def delete_logs():
    delete_old_logs(3)


@shared_task
def mailing_all():
    mailing()
