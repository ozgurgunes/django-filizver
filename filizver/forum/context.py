from django.conf import settings

from filizver.forum import defaults


def defaults(request):
    return {
        'defaults': defaults,
        'DEBUG': settings.DEBUG,
    }
