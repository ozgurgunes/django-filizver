# -*- coding: utf-8 -*-
import re
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from manifest.accounts.models import BaseUser
from filizver.managers.user import UserManager
from filizver.models.topic import Topic
from filizver.plugins.user import UserEntry

class User(AbstractUser, BaseUser):
    
    topic = models.OneToOneField(Topic, related_name='user_entry', blank=True, null=True)

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        app_label='filizver'

    def get_topic(self):
        topic, created = Topic.objects.get_or_create(user=self, plugin=UserEntry().get_model())
        return topic
        
    def save(self, *args, **kwargs):
        if self.id and not self.topic:
            self.topic = self.get_topic()
        super(User, self).save(*args, **kwargs)
        