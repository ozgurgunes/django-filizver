# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from filizver.core.models import UserMixin
from filizver.topic.models import Topic


class Entry(UserMixin):
    """
    Extension class for Topic object
    """
    content_type            = models.ForeignKey(ContentType, related_name='entries')
    object_id               = models.PositiveIntegerField()
    content_object          = generic.GenericForeignKey()

    user                    = models.ForeignKey(User, related_name='entries')
    topic                   = models.ForeignKey(Topic, related_name='entries')
    
    position                = models.PositiveSmallIntegerField(blank=True, null=False, default=0, editable=False);
    
    #plugins                 = ManyPluginField(EntryPoint)

    class Meta:
        app_label                = 'filizver'
        ordering                = ('position', '-created_date',)
        verbose_name            = _('Entry')
        verbose_name_plural     = _('Entries')
        get_latest_by           = 'created_date'

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
            return u"%s/_entry_detail.html" % self.content_type.name.lower()



class EntryBase(UserMixin):
    """Abstract base class for entry contents"""

    user            = models.ForeignKey(User, related_name='%(class)s_set', blank=False, null=False)
    topic           = models.ForeignKey(Topic, related_name='%(class)s_set', blank=False, null=False)
    
    class Meta:
        abstract        = True
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
            return u"%s/_entry_list.html" % self._meta.module_name.lower()
        elif template == 'detail':
            return u"%s/_entry_detail.html" % self._meta.module_name.lower()
        else:    
            return u"%s/_entry.html" % self._meta.module_name.lower()



def add_entry_signal(sender, instance, user=None, topic=None, created_date=None, **kwargs):
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
            'created_date': datetime.datetime.now()
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


post_delete.connect(delete_entry_object_signal, sender=Entry)
