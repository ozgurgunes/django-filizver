#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models

class Command(BaseCommand):
    args = ''
    help = 'Migrate forum profiles to local site profile'

    def handle(self, *args, **options):
        profile_app, profile_model = settings.AUTH_PROFILE_MODULE.split('.')
        profile_model = ContentType.objects.get(app_label=profile_app, model=profile_model).model_class()
        for user in User.objects.all():
            #print(u'migrating profile for %s\n' % user.username)
            forum_profile = user.forum_profile
            try:
                profile = user.get_profile()
            except profile_model.DoesNotExist:
                profile = profile_model(user=user)
            profile.avatar = forum_profile.avatar
            profile.signature = forum_profile.signature
            profile.signature_html = forum_profile.signature_html
            profile.time_zone = forum_profile.time_zone
            profile.language = forum_profile.language
            profile.show_signatures = forum_profile.show_signatures
            profile.markup = forum_profile.markup
            profile.post_count = forum_profile.post_count
            profile.avatar = forum_profile.avatar
            profile.save()
        self.stdout.write('All profiles successfuly migrated')
