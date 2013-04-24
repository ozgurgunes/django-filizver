# -*- coding: utf-8 -*-
from django.db.models import Manager, Q
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

from manifest.accounts.managers import BaseUserManager

class BaseQuerySet(QuerySet):
    pass
    

class UserManager(BaseUserManager):
    pass
    
    
class BaseManager(Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
            return BaseQuerySet(self.model, using=self._db)    


class TopicQuerySet(QuerySet):

    def published(self):
        return self.filter(deleted=False)


class TopicManager(BaseManager):

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


class EntryManager(BaseManager):
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
            return qs.order_by('-created_date')[0].created_date
        except IndexError:
            return datetime.fromtimestamp(0)
