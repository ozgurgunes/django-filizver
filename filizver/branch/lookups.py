# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

from selectable.base import ModelLookup
from selectable.registry import registry

from filizver.topic.models import Topic
from filizver.branch.models import Branch


class BranchLookup(ModelLookup):
    model   = Topic
    search_fields = ['title__icontains',]
    
    def get_query(self,request,q):
        """
        Return a query set.  you also have access to request.user if needed
        
        """
        topic_id = request.GET.get('topic', None)
        branches_qs = Branch.objects.filter(topic__pk=topic_id).values_list('source')
        return Topic.objects.exclude(pk=topic_id).exclude(pk__in=branches_qs).filter(
                                models.Q(title__istartswith=q) | models.Q(slug__istartswith=q))

    def get_item_id(self,item):
        # The id is the value that will eventually be returned by the field/widget. 
        return item.pk

    def get_item_label(self,item):
        # The value is shown in the input once the item has been selected. 
        return mark_safe(u'%s<br/><small>%s - %s</small>' % (item.title, item.user, item.created_date))


registry.register(BranchLookup)
