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

    def for_user(self, user):
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

class EntryManager(models.Manager):
    """
    Managers for the Filizver Entry model

    def __init__(self):
        super(EntryManager, self).__init__()
        self.models_by_name = {}

    """

    def get_for_model(self, model):
        """
        Return a QuerySet of only items of a certain type.
        """
        return self.filter(content_type=ContentType.objects.get_for_model(model))

    def get_last_update_of_model(self, model, **kwargs):
        """
        Return the last time a given model's items were updated. Returns the epoch if the items were never updated.
        """
        qs = self.get_for_model(model)
        if kwargs:
            qs = qs.filter(**kwargs)
        try:
            return qs.order_by('-date_created')[0].date_created
        except IndexError:
            return datetime.fromtimestamp(0)
