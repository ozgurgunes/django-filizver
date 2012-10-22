from django.conf import settings

from filizver.forum import defaults as forum_defaults


def defaults(request):
    return {
        'defaults': forum_defaults,
        'DEBUG': settings.DEBUG,
    }
