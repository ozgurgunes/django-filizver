# -*- coding: utf-8 -*-
import re
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

from djangoplugins.fields import PluginField
from manifest.accounts.models import BaseUser

from filizver.managers import TopicManager, UserManager
from filizver.utils.models import UserMixin
from filizver.plugins import EntryPoint
from filizver.utils import defaults
from filizver.utils.core import get_upload_to
from filizver.utils.text import MARKUP_CHOICES


class BaseTopic(UserMixin):

    title                   = models.CharField(_('Title'), max_length=216)
    slug                    = models.SlugField(_('Slug'), max_length=216, blank=True)
    body                    = models.TextField(_('Body'), blank=True)
    url                     = models.URLField(_('URL'), blank=True)
    file                    = models.FileField(upload_to=get_upload_to, blank=True)
    image                   = models.ImageField(upload_to=get_upload_to, blank=True, 
                                            width_field='image_width', height_field='image_height')
        
    image_width             = models.IntegerField(editable=False, blank=True, null=True)
    image_height            = models.IntegerField(editable=False, blank=True, null=True)

    parent                  = models.ForeignKey('self', blank=True, null=True)
    position                = models.IntegerField(_('Position'), default=1, blank=True, null=True)

    plugin                  = PluginField(EntryPoint)
    
    class Meta:
        abstract                = True
        verbose_name            = _('topic')
        verbose_name_plural     = _('topics')
        ordering                = ('-created_date', 'title')
        get_latest_by           = 'created_date'

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(slugify(self.title))
        # if not self.parent:
        #     self.parent = super(BaseTopic, self).objects.get_or_create(pk=0, title='System')
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

    
class Topic(BaseTopic):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey('User', related_name='topics')    

    moderators              = models.ManyToManyField('User', verbose_name=_('Moderators'), 
                                        through='Moderator', related_name='moderating',
                                        blank=True, null=True)
    
    objects                 = TopicManager()

    class Meta:
        app_label           = 'filizver'
        
    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('filizver:topic_detail', None, {
            'username': self.user.username,
            'slug': self.slug,
            'pk': self.pk
            })


class Moderator(models.Model):
    
    user            = models.ForeignKey('User')
    topic           = models.ForeignKey('Topic')
    
    class Meta:
        app_label               = 'filizver'
        unique_together = (('user', 'topic'),)

class User(AbstractUser, BaseUser):
    
    topic = models.OneToOneField(Topic, related_name='user_entry', blank=True, null=True)

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        # app_label='filizver'

    def get_topic(self):
        topic, created = Topic.objects.get_or_create(user=self, plugin=UserEntry().get_model())
        return topic
        
    def save(self, *args, **kwargs):
        if self.id and not self.topic:
            self.topic = self.get_topic()
        super(User, self).save(*args, **kwargs)        


class AbstractEntry(Topic):

    topic = models.OneToOneField(Topic, parent_link=True)

    class Meta:
        abstract        = True
        app_label       = 'filizver'
        ordering        = ('-created_date',)
        get_latest_by   = 'created_date'

    @models.permalink
    def get_absolute_url(self):
        return ('filizver_%s_detail' % self._meta.module_name.lower, None, {'id': self.id })

    def get_update_url(self):
        return ('filizver_%s_update' % self._meta.module_name.lower, None, {'id': self.id })

    def get_delete_url(self):
        return ('filizver_%s_delete' % self._meta.module_name.lower, None, {'id': self.id })

    def entry_template(self, template=None):
        if template == 'list':
            return u"%s/%s_entry_list.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())
        elif template == 'detail':
            return u"%s/%s_entry_detail.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())
        else:    
            return u"%s/%s_entry.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())


class Text(AbstractEntry):

    html            = models.TextField(_('HTML'), blank=True, null=True)
    markup          = models.CharField(_('Markup'), max_length=15, 
                            choices=MARKUP_CHOICES, default=defaults.DEFAULT_MARKUP)

    class Meta:
        verbose_name            = _('text')
        verbose_name_plural     = _('texts')

    def __unicode__(self):
        return u"%s" % self.body[:64] + '...' if len(self.body) > 64 else ''

    def save(self, *args, **kwargs):
        self.html = utils.text_to_html(self.body, self.markup)
        if defaults.SMILEYS_SUPPORT: #and self.user.profile.smileys:
            self.html = utils.smileys(self.html)
        super(Text, self).save(*args, **kwargs)


class Picture(AbstractEntry):
    """
    Photo model
    """

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    alt             = models.CharField(max_length=128, blank=True, null=True)
    caption         = models.TextField(blank=True, null=True)

    display         = models.CharField(max_length=1, blank=True, null=True,
                            choices=DISPLAY_CHOICES, default='N')

    class Meta:
        verbose_name            = _('image')
        verbose_name_plural     = _('images')

    def __unicode__(self):
        return u"%s" % self.image


class Link(AbstractEntry):
    
    class Meta:
        verbose_name            = _('link')
        verbose_name_plural     = _('links')

    def __unicode__(self):
        return u"%s" % self.url


class Document(AbstractEntry):
    """Photo model"""

    class Meta:
        verbose_name            = _('document')
        verbose_name_plural     = _('documents')

    def __unicode__(self):
        return u"%s" % self.source

class Video(AbstractEntry):

    embed           = models.TextField(_('Embed'), blank=True, null=True)

    class Meta:
        verbose_name            = _('video')
        verbose_name_plural     = _('videos')

    def __unicode__(self):
        return u"%s" % self.file or self.url or self.embed


class Sound(AbstractEntry):

    embed           = models.TextField(_('Embed'), blank=True, null=True)

    class Meta:
        verbose_name            = _('Sound')
        verbose_name_plural     = _('Sounds')

    def __unicode__(self):
        return u"%s" % self.file or self.url or self.embed
