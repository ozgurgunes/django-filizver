# -*- coding: utf-8 -*-
import re
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag
from django.template.defaultfilters import slugify
from filizver.topic.plugins import TopicInline
from filizver.core.models import DateMixin, DeleteMixin

from djangoplugins.fields import ManyPluginField

class Topic(DateMixin, DeleteMixin):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(User, related_name='topics')
    
    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True, null=False)

    active                  = models.BooleanField(_('Active'), default=True)
    
    branches                = models.ManyToManyField('self', blank=True, null=True, 
                                        symmetrical=False, through='Branch', 
                                        related_name='sources')

    followers               = models.ManyToManyField(User, verbose_name=_('Followers'), 
                                        through='Follower', related_name='following',
                                        blank=True, null=True)
    moderators              = models.ManyToManyField(User, verbose_name=_('Moderators'), 
                                        through='Moderator', related_name='moderating',
                                        blank=True, null=True)
    

    ip_address              = models.IPAddressField(_('IP Address'), editable=False, 
                                        blank=False, null=False)
    api_gateway             = models.IPAddressField(_('API Gateway'), editable=False, 
                                        blank=True, null=True)

    tags                    = TagField()
    #objects                 = TopicManager()
    
    plugins                 = ManyPluginField(TopicInline, blank=True, null=True,)
    
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
            'id': self.pk
            })

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    tag_list = property(_get_tags, _set_tags)
    
    def extend(self, model, *args, **kwargs):
        try:
            obj = model.objects.get(parent_id=self.id)
        except model.DoesNotExist:            
            obj = model(parent_id=self.id)
            obj.__dict__.update(self.__dict__, **kwargs)
            obj.save()
        return obj
    