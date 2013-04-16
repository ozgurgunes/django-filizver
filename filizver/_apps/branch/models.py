# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from filizver.topic.models import Topic
from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal


class Branch(EntryBase):
    """
    Component class for Topic object
    """
    source                  = models.ForeignKey(Topic, related_name='source_set')
    
    class Meta:
        app_label                = 'filizver'
        unique_together = (('source', 'topic'),)
        verbose_name            = _('Branch')
        verbose_name_plural     = _('Branches')

    def __unicode__(self):
        return u"%s > %s" % (self.topic, self.source)


post_save.connect(add_entry_signal, sender=Branch)
post_delete.connect(delete_entry_signal, sender=Branch)
