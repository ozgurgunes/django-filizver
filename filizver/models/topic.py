# -*- coding: utf-8 -*-
import re
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

from djangoplugins.fields import PluginField

from tagging.models import Tag
from tagging.fields import TagField

from filizver.managers import TopicManager
from filizver.models.base import UserMixin
from filizver.plugins.entry import EntryPoint
from filizver.utils.core import get_upload_to


class TaggingMixin(models.Model):

    tags                    = TagField()
    
    class Meta:
        abstract = True

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    tag_list = property(_get_tags, _set_tags)


class BaseTopic(UserMixin):

    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True, null=False)
    body                    = models.TextField(_('Body'), blank=False, null=False)
    url                     = models.URLField(_('URL'), blank=False, null=False)
    file                    = models.FileField(upload_to=get_upload_to, blank=False, null=False)
    image                   = models.ImageField(upload_to=get_upload_to, blank=False, null=False, 
                                            width_field='image_width', height_field='image_height')
        
    image_width             = models.IntegerField(editable=False, null=True)
    image_height            = models.IntegerField(editable=False, null=True)

    parent                  = models.ForeignKey('self', default=0, blank=False, null=False)
    position                = models.IntegerField(_('Position'), default=1, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name            = _('topic')
        verbose_name_plural     = _('topics')
        ordering                = ('-created_date', 'title')
        get_latest_by           = 'created_date'

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(slugify(self.title))
        super(BaseTopic, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete uploaded files first
        if self.image:
            delete(self.image)
        if self.file:
            delete(self.file)
        super(BaseTopic, self).delete()

    def extend(self, model, *args, **kwargs):
        # Extend topic to inheriting model
        try:
            obj = model.objects.get(parent_id=self.id)
        except model.DoesNotExist:            
            obj = model(parent_id=self.id)
            obj.__dict__.update(self.__dict__, **kwargs)
            obj.save()
        return obj

    
class Topic(BaseTopic, TaggingMixin):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(get_user_model(), related_name='topics')    

    followers               = models.ManyToManyField(get_user_model(), verbose_name=_('Followers'), 
                                        through='Follower', related_name='following',
                                        blank=True, null=True)
    moderators              = models.ManyToManyField(get_user_model(), verbose_name=_('Moderators'), 
                                        through='Moderator', related_name='moderating',
                                        blank=True, null=True)
    
    objects                 = TopicManager()

    class Meta:
        app_label               = 'filizver'

        
    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('filizver:topic_detail', None, {
            'username': self.user.username,
            'slug': self.slug,
            'pk': self.pk
            })
    
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


