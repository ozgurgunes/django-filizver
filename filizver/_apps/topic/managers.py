# -*- coding: utf-8 -*-
import operator
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


class TopicQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(deleted=False)


class TopicManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
            return TopicQuerySet(self.model, using=self._db)    

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

