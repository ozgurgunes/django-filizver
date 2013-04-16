# -*- coding: utf-8 -*-
import operator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from relationships.utils import positive_filter


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
            return qs.order_by('-created_date')[0].created_date
        except IndexError:
            return datetime.fromtimestamp(0)
