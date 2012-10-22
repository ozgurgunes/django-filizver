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
from djangoplugins.fields import ManyPluginField

class Topic(models.Model):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(User, related_name='topics')
    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True, null=False)

    created_date            = models.DateTimeField(_('Created date'), auto_now_add=True, 
                                        blank=False, null=False)
    updated_date            = models.DateTimeField(_('Updated date'), auto_now=True, 
                                        blank=True, null=True)
    deleted_date            = models.DateTimeField(_('Deleted date'), blank=True, null=True)

    active                  = models.BooleanField(_('Active'), default=True)
    deleted                 = models.BooleanField(_('Deleted'), default=False)
    
    moderators              = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Moderators'))
    

    # ip                      = models.IPAddressField(_('IP Address'), blank=False, null=False, editable=False)
    # api                     = models.IPAddressField(_('API Gateway'), blank=False, null=False editable=False)

    # branches                = models.ManyToManyField('self', blank=True, null=True, 
    #                                     symmetrical=False, through='Branch', 
    #                                     related_name='sources')

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
        
    def delete(self, commit=False, *args, **kwargs):
        if commit:
            super(Topic, self).delete(*args, **kwargs)
        else:
            self.deleted = True
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('filizver_topic_detail', None, {
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
    