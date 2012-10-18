# -*- coding: utf-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.models import EntryBase, add_entry_signal, delete_entry_signal


def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), str(instance._meta.module_name), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


class Picture(EntryBase):
    """Photo model"""

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    source          = models.ImageField(upload_to=get_upload_to, blank=False, null=False, 
                            width_field='picture_width', height_field='picture_height')
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    display         = models.CharField(max_length=1, blank=True, null=True,
                            choices=DISPLAY_CHOICES, default='N')

    picture_width     = models.IntegerField(editable=False, null=True)
    picture_height    = models.IntegerField(editable=False, null=True)

    class Meta:
        verbose_name            = _('Photo')
        verbose_name_plural     = _('Photos')

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        delete(self.source)
        super(Photo, self).delete()


post_save.connect(add_entry_signal, sender=Picture)
post_delete.connect(delete_entry_signal, sender=Picture)

