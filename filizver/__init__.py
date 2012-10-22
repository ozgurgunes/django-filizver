# -*- coding: utf-8 -*-
from django.db import transaction
from django.contrib.auth.models import User
from manifest.accounts.signals import activation_complete
from filizver.topic.models import Topic

@transaction.commit_on_success()
def createTopic(sender, user, **kwargs):
    """
    Create a UserProfile object each time a User is created.
    """
    topic, created = Topic.objects.get_or_create(user=user, title=user.username)    
activation_complete.connect(createTopic)

