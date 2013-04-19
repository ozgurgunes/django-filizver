# -*- coding: utf-8 -*-
from django.db.models import Manager
from django.db.models.query import QuerySet

class BaseQuerySet(QuerySet):
    pass
    

class BaseManager(Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
            return BaseQuerySet(self.model, using=self._db)    
