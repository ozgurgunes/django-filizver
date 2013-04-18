# -*- coding: utf-8 -*-
import re
import datetime
from mongoengine import *
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from user import User
from entry import Entry
from core import UserMixin


class Topic(DynamicDocument, UserMixin):
    """
    Topic class for Filizver application
    """
    user                    = ReferenceField(User, required=True)
    
    title                   = StringField(max_length=216, required=True)
    slug                    = StringField(max_length=216, required=True)
    
    entries                 = ListField(EmbeddedDocumentField(Entry))

    active                  = BooleanField(default=True)
    
    followers               = ListField(ReferenceField(User))
    moderators              = ListField(ReferenceField(User))
    
    tags                    = ListField(StringField())
    
    meta = {
        'ordering': ['-created_date',],
        'allow_inheritance': True,
        'indexes': ['title',]
        }
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(slugify(self.title))
        super(Topic, self).save(*args, **kwargs)         
    
    #@models.permalink
    def get_absolute_url(self):
        return ('filizver:topic_detail', None, {
            'username': self.user.username,
            'slug': self.slug,
            'pk': self.pk
            })
    
    