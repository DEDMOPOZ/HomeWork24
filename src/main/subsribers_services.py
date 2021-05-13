from .models import Subscriber


def sub_all():
    all_subs = Subscriber.objects.all()
    return all_subs
