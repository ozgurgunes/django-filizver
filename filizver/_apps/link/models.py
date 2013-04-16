# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal
from filizver.core.utils import get_upload_to

class Link(EntryBase):
    url             = models.URLField(_('URL'), blank=False, null=False)
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)
    image           = models.ImageField(upload_to=get_upload_to, blank=True, null=True, 
                            width_field='image_width', height_field='image_height')
    image_width     = models.IntegerField(editable=False, null=True)
    image_height    = models.IntegerField(editable=False, null=True)
    
    class Meta:
        app_label               = 'filizver'
        verbose_name            = _('Link')
        verbose_name_plural     = _('Links')

    def __unicode__(self):
        return u"%s" % self.url

    def delete(self):
        delete(self.image)
        super(Link, self).delete()


post_save.connect(add_entry_signal, sender=Link)
post_delete.connect(delete_entry_signal, sender=Link)

