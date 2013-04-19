# -*- coding: utf-8 -*-
import re
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

# from tagging.models import Tag
# from tagging.fields import TagField

from filizver.managers import TopicManager
from core import UserMixin


class Topic(UserMixin):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(get_user_model(), related_name='topics')
    
    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True, null=False)

    active                  = models.BooleanField(_('Active'), default=True)
    
    followers               = models.ManyToManyField(get_user_model(), verbose_name=_('Followers'), 
                                        through='Follower', related_name='following',
                                        blank=True, null=True)
    moderators              = models.ManyToManyField(get_user_model(), verbose_name=_('Moderators'), 
                                        through='Moderator', related_name='moderating',
                                        blank=True, null=True)
    
    #tags                    = TagField()
    
    objects                 = TopicManager()
        
    class Meta:
        app_label               = 'filizver'
        ordering                = ('-created_date', 'title')
        verbose_name            = _('Topic')
        verbose_name_plural     = _('Topics')
        get_latest_by           = 'created_date'

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(slugify(self.title))
        super(Topic, self).save(*args, **kwargs)         

    @models.permalink
    def get_absolute_url(self):
        return ('filizver:topic_detail', None, {
            'username': self.user.username,
            'slug': self.slug,
            'pk': self.pk
            })

    # def _get_tags(self):
    #     return Tag.objects.get_for_object(self)
    # def _set_tags(self, tags):
    #     Tag.objects.update_tags(self, tags)
    # tag_list = property(_get_tags, _set_tags)
    

class Follower(models.Model):
    
    user            = models.ForeignKey(get_user_model())
    topic           = models.ForeignKey(Topic)
    
    class Meta:
        app_label           = 'filizver'
        unique_together     = (('user', 'topic'),)


class Moderator(models.Model):
    
    user            = models.ForeignKey(get_user_model())
    topic           = models.ForeignKey(Topic)
    
    class Meta:
        app_label               = 'filizver'
        unique_together = (('user', 'topic'),)


