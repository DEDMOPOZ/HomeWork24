from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import requests

from .subsribers_services import sub_all


def notify(email_to, number):
    email_send(email_to, "author")
    telegram_notify(number)


def email_send(email_to, author):

    send_mail(
        "Subscription",
        "You have subscribed on Author: {}".format(author),
        EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )


def mailing():
    subscribers = sub_all()
    emails = list(subscribers.values_list("email_to", flat=True).distinct())
    url = "https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php"
    text = requests.get(url).text
    print(emails)

    send_mail(
        "Subscribers mailing",
        text,
        EMAIL_HOST_USER,
        emails,
        fail_silently=False,
    )


def telegram_notify(number):
    pass
