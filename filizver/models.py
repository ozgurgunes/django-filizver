# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from tagging.fields import TagField
from tagging.models import Tag
from manifest.core.models import SlugifyUniquely
from filizver.managers import TopicManager

class Topic(models.Model):
    """
    Topic class for Filizver application
    """
    user                    = models.ForeignKey(User)
    title                   = models.CharField(max_length=216)
    slug                    = models.SlugField(max_length=216, blank=True, null=False)
    date_created            = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    is_public               = models.BooleanField(default=True)

    branches                = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, through='Branch', related_name='sources')

    tags                    = TagField()
    objects                 = TopicManager()
    
    class Meta:
        ordering                = ('-date_created', 'title')
        verbose_name            = _('Topic')
        verbose_name_plural     = _('Topics')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(SlugifyUniquely(self.title, self.__class__)) #str(slugify(self.title))
        super(Topic, self).save(*args, **kwargs) 
        
    def delete(self):
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
        Tag.objects.update_tags(self, tag_list)

    tag_list = property(_get_tags, _set_tags)

class Post(models.Model):
    """
    Extension class for Topic object
    """
    content_type            = models.ForeignKey(ContentType)
    object_id               = models.PositiveIntegerField()
    content_object          = generic.GenericForeignKey()
        

    user                    = models.ForeignKey(User)
    topic                  = models.ForeignKey(Topic)
    date_created            = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    
    position                = models.PositiveSmallIntegerField(blank=True, null=False, default=0, editable=False);
    
    class Meta:
        ordering                = ('position', '-date_created',)
        verbose_name            = _('Post')
        verbose_name_plural     = _('Posts')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s" % self.content_object
        
    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.position = Post.objects.filter(topic=self.topic).aggregate(models.Max('position'))['position__max'] + 1
            except:
                self.position = 1
        super(Post, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', None, {
            'post_pk': self.pk,
            })

    def list_template(self):
        try:
            return self.content_object.post_template('list')
        except AttributeError:
            return u"%s/_%s_post_list.html" % (self.content_type.app_label, self.content_type.name.lower())

    def detail_template(self):
        try:
            return self.content_object.post_template('detail')
        except AttributeError:
            return u"%s/_%s_post_detail.html" % (self.content_type.app_label, self.content_type.name.lower())

class PostBase(models.Model):
    """Abstract base class for post contents"""

    user            = models.ForeignKey(User, blank=False, null=False)
    topic          = models.ForeignKey(Topic, blank=False, null=False)
    date_created    = models.DateTimeField(blank=True, null=False, auto_now_add=True)

    class Meta:
        abstract        = True
        ordering        = ('-date_created',)
        get_latest_by   = 'date_created'

    def post_template(self, template=None):
        if template == 'list':
            return u"%s/_%s_post_list.html" % (self._meta.app_label, self._meta.module_name.lower())
        elif template == 'detail':
            return u"%s/_%s_post_detail.html" % (self._meta.app_label, self._meta.module_name.lower())
        else:    
            return u"%s/_%s_post.html" % (self._meta.app_label, self._meta.module_name.lower())

class Branch(PostBase):
    """
    Component class for Topic object
    """
    source                  = models.ForeignKey(Topic, related_name='source_set')
    
    class Meta:
        unique_together = (('source', 'topic'),)
        verbose_name            = _('Branch')
        verbose_name_plural     = _('Branches')

    def __unicode__(self):
        return u"%s > %s" % (self.topic, self.source)
        