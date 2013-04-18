# -*- coding: utf-8 -*-
import re
import datetime
from mongoengine import *
from django.utils.translation import ugettext_lazy as _

from filizver.utils import defaults
from user import User
#from topic import Topic
from core import UserMixin


class Entry(DynamicEmbeddedDocument, UserMixin):
    """
    Extension class for Topic object
    """
    user                    = ReferenceField(User, required=True)    
    position                = IntField(required=True);
    
    meta = {
        'ordering': ['position', '-created_date',],
        'allow_inheritance': True,
        }
        
    @property
    def entry_type(self):
        return self.__class__.__name__

    def __unicode__(self):
        return u"%s" % self.pk
        
    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                self.position = Entry.objects.filter(topic=self.topic).aggregate(models.Max('position'))['position__max'] + 1
            except:
                self.position = 1
        super(Entry, self).save(*args, **kwargs)


class Branch(Entry):
    
    source  = ReferenceField(Topic)

    def __unicode__(self):
        return u"%s > %s" % (self.topic, self.source)
            

class Text(Entry):

    MARKUP_CHOICES = []
    try:
        import markdown
        MARKUP_CHOICES.append(("markdown", "Markdown"))
    except ImportError:
        pass
    try:
        import textile
        MARKUP_CHOICES.append(("textile", "Textile"))
    except ImportError:
        pass
    try:
        import postmarkup
        MARKUP_CHOICES.append(('bbcode', 'BBCode'))
    except ImportError:
        pass
    
    body            = StringField(required=True)
    html            = StringField()
    markup          = StringField(max_length=15, choices=MARKUP_CHOICES, default=defaults.DEFAULT_MARKUP)

    def __unicode__(self):
        return u"%s" % self.body[:64] + '...' if len(self.body) > 64 else ''

    def save(self, *args, **kwargs):
        self.html = utils.text_to_html(self.body, self.markup)
        if defaults.SMILEYS_SUPPORT: #and self.user.profile.smileys:
            self.html = utils.smileys(self.html)
        super(Text, self).save(*args, **kwargs)


class Image(Entry):

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    source          = ImageField(required=True)
    title           = StringField(max_length=128)
    description     = StringField()

    display         = StringField(max_length=1, choices=DISPLAY_CHOICES, default='N')

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        self.source.delete()
        super(Image, self).delete()


class Link(Entry):

    url             = URLField(required=True)
    title           = StringField(max_length=216)
    description     = StringField()
    
    def __unicode__(self):
        return u"%s" % self.url


class Document(Entry):
    """Photo model"""

    source          = FileField(required=True)
    title           = StringField(max_length=216)
    description     = StringField()

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        self.source.delete()
        super(Document, self).delete()


class Video(Entry):
    """Photo model"""

    source          = FileField()
    url             = URLField()
    embed           = StringField()
    title           = StringField(max_length=216)
    description     = StringField()

    def __unicode__(self):
        return u"%s" % self.source or self.url or self.embed

    def save(self, *args, **kwargs):
        if self.source is None and self.url is None and self.embed is None:
            self.error('At least one field is required.')
    
    def delete(self):
        self.source.delete()
        super(Video, self).delete()

