from time import time

from .models import Logger


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        st = time()

        response = self.get_response(request)

        utm = request.GET.get("utm")
        time_execution = time() - st
        ip = get_client_ip(request)

        if utm:
            logger = Logger(time_execution=time_execution, path=request.path, utm=utm, ip=ip)
            logger.save()
        else:
            logger = Logger(time_execution=time_execution, path=request.path, utm="", ip=ip)
            logger.save()

        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        ip = request.META.get("HTTP_X_REAL_IP")
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
