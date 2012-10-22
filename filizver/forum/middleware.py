from datetime import datetime, timedelta

from django.core.cache import cache
from django.utils import translation
from django.conf import settings as global_settings

import defaults

class LastLoginMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            cache.set('djangobb_user%d' % request.user.id, True, defaults.USER_ONLINE_TIMEOUT)

class ForumMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            language = translation.get_language_from_request(request)

            if not profile.locale:
                profile.locale = language
                profile.save()

            if profile.locale and profile.locale != language:
                request.session['django_language'] = profile.locale
                translation.activate(profile.locale)
                request.LANGUAGE_CODE = translation.get_language()