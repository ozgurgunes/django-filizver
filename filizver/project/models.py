# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from filizver.topic.models import Topic


class Project(models.Model):
    topic           = models.OneToOneField(Topic, parent_link=True, related_name='projects')
    description     = models.TextField(_('Description'), blank=True, default='')
    moderators      = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Moderators'))

    class Meta:
        ordering = ['topic__title']
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return self.topic.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('project:project_detail', [self.id])

