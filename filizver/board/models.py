# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from filizver.topic.models import Topic


class Board(models.Model):
    topic           = models.OneToOneField(Topic, parent_link=True, related_name='boards')
    description     = models.TextField(_('Description'), blank=True, default='')
    moderators      = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Moderators'))

    class Meta:
        ordering = ['topic__title']
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')

    def __unicode__(self):
        return self.topic.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('board:board_detail', [self.id])

