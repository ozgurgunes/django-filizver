# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from filizver.topic.models import Topic

class Moderator(models.Model):
    
    user            = models.ForeignKey(User, related_name='moderators')
    topic           = models.ForeignKey(Topic, related_name='moderators')
    
    objects                 = managers.FavoriteManager()

