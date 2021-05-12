from datetime import timedelta

from django.utils import timezone

from .models import Logger


def all_logs():
    all_logs = Logger.objects.all()
    return all_logs


def delete_old_logs(days):
    time_threshold = timezone.now() - timedelta(days=days)
    logs = Logger.objects.filter(created__lte=time_threshold)
    logs.delete()
