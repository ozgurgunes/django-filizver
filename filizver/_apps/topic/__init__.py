# -*- coding: utf-8 -*-
from manifest.accounts.signals import activation_complete
from filizver.topic.models import Topic


def createTopic(sender, user, **kwargs):
    """
    Create a UserProfile object each time a User is created.
    """
    topic, created = Topic.objects.get_or_create(user=user, title=user.username)    


activation_complete.connect(createTopic)
