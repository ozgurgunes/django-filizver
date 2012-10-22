# -*- coding: utf-8 -*-
import operator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from relationships.utils import positive_filter

class TopicManager(models.Manager):
    """
    Topic manager
    
    def get_query_set(self):
        # Get active objects only everytime.
        return super(TopicManager,  self).get_query_set().filter(is_public=True)

    """        

    def timeline(self, user):
        user_list = User.objects.filter(username=user.username) | user.relationships.following()
        return positive_filter(super(TopicManager, self).all(), user_list)

    def search(self, search_terms):
        from libs.search import normalize
        terms = normalize(search_terms)
        q_objects = []
        
        for term in terms:
            q_objects.append(models.Q(title__icontains=term))
            q_objects.append(models.Q(tags__icontains=term))
        
        # Start with a bare QuerySet
        qs = self.get_query_set()
        
        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))

