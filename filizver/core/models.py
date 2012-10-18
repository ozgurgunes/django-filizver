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


class Topic(models.Model):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(User, related_name='topics')
    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True, null=False)

    create_date             = models.DateTimeField(_('Create Date'), auto_now_add=True, 
                                        blank=False, null=False)
    update_date             = models.DateTimeField(_('Update Date'), auto_now=True, 
                                        blank=True, null=True)
    delete_date             = models.DateTimeField(_('Delete Date'), blank=True, null=True)

    active                  = models.BooleanField(_('Active'), default=True)
    deleted                 = models.BooleanField(_('Deleted'), default=False)

    user_ip                 = models.IPAddressField(_('User IP'), blank=False, null=False)

    # branches                = models.ManyToManyField('self', blank=True, null=True, 
    #                                     symmetrical=False, through='Branch', 
    #                                     related_name='sources')

    tags                    = TagField()
    objects                 = TopicManager()
    
    plugins                 = PluginField(EntryType, blank=True, null=True,)
    
    class Meta:
        ordering                = ('-create_date', 'title')
        verbose_name            = _('Topic')
        verbose_name_plural     = _('Topics')
        get_latest_by           = 'create_date'

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(slugify(self.title))
        super(Topic, self).save(*args, **kwargs) 
        
    def delete(self, *args, **kwargs):
        super(Topic, self).delete()

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
    

