# -*- coding: utf-8 -*-
import re
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.db.models.signals import post_save, post_delete
from tagging.fields import TagField
from tagging.models import Tag
from manifest.core.models import SlugifyUniquely
from filizver.managers import TopicManager


def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), str(instance._meta.module_name), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


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


class Entry(models.Model):
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
        verbose_name            = _('Entry')
        verbose_name_plural     = _('Entries')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s" % self.content_object
        
    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.position = Entry.objects.filter(topic=self.topic).aggregate(models.Max('position'))['position__max'] + 1
            except:
                self.position = 1
        super(Entry, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('entry_detail', None, {
            'entry_pk': self.pk,
            })

    def list_template(self):
        try:
            return self.content_object.entry_template('list')
        except AttributeError:
            return u"%s/_%s_entry_list.html" % (self.content_type.app_label, self.content_type.name.lower())

    def detail_template(self):
        try:
            return self.content_object.entry_template('detail')
        except AttributeError:
            return u"%s/_%s_entry_detail.html" % (self.content_type.app_label, self.content_type.name.lower())



class EntryBase(models.Model):
    """Abstract base class for entry contents"""

    user            = models.ForeignKey(User, blank=False, null=False)
    topic          = models.ForeignKey(Topic, blank=False, null=False)
    date_created    = models.DateTimeField(blank=True, null=False, auto_now_add=True)

    class Meta:
        abstract        = True
        ordering        = ('-date_created',)
        get_latest_by   = 'date_created'

    @models.permalink
    def get_absolute_url(self):
        return ('filizver_%s_detail' % self._meta.module_name.lower, None, {'id': self.id })

    def get_update_url(self):
        return ('filizver_%s_update' % self._meta.module_name.lower, None, {'id': self.id })

    def get_delete_url(self):
        return ('filizver_%s_delete' % self._meta.module_name.lower, None, {'id': self.id })

    def entry_template(self, template=None):
        if template == 'list':
            return u"%s/_%s_entry_list.html" % (self._meta.app_label, self._meta.module_name.lower())
        elif template == 'detail':
            return u"%s/_%s_entry_detail.html" % (self._meta.app_label, self._meta.module_name.lower())
        else:    
            return u"%s/_%s_entry.html" % (self._meta.app_label, self._meta.module_name.lower())


class Branch(EntryBase):
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



class Text(EntryBase):
    """Passage model"""

    source            = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name            = _('Text')
        verbose_name_plural     = _('Texts')

    def __unicode__(self):
        return u"%s" % self.source
        

class Image(EntryBase):
    """Photo model"""

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    source          = models.ImageField(upload_to=get_upload_to, blank=False, null=False, 
                            width_field='image_width', height_field='image_height')
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    display         = models.CharField(max_length=1, blank=True, null=True,
                            choices=DISPLAY_CHOICES, default='N')

    image_width     = models.IntegerField(editable=False, null=True)
    image_height    = models.IntegerField(editable=False, null=True)

    class Meta:
        verbose_name            = _('Photo')
        verbose_name_plural     = _('Photos')

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        delete(self.source)
        super(Photo, self).delete()


def add_entry_signal(sender, instance, user=None, topic=None, date_created=None, **kwargs):
	"""
	This is a generic singal for adding an object to the Topic.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	obj, created = Entry.objects.get_or_create(
		content_type=ctype,
		object_id=instance.id,
        defaults={
            'user': instance.user,
            'topic': instance.topic,
            'date_created': datetime.datetime.now()
            })


def delete_entry_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related Entry when an object is deleted.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	try:
		entry = Entry.objects.get(content_type=ctype, object_id=instance.id)
		entry.delete()
	except Entry.MultipleObjectsReturned:
		entries = Entry.objects.filter(content_type=ctype, object_id=instance.id)
		for entry in entries:
			entry.delete()
	except Entry.DoesNotExist:
		pass


def delete_entry_object_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related object when a Entry is deleted.

	"""
	try:
	    instance.content_object.delete()
	except:
	    pass


post_save.connect(add_entry_signal, sender=Branch)
post_save.connect(add_entry_signal, sender=Text)
post_save.connect(add_entry_signal, sender=Image)
post_delete.connect(delete_entry_signal, sender=Branch)
post_delete.connect(delete_entry_signal, sender=Text)        
post_delete.connect(delete_entry_signal, sender=Image)
post_delete.connect(delete_entry_object_signal, sender=Entry)
