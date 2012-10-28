# -*- coding: utf-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal
from filizver.core.utils import get_upload_to


class Image(EntryBase):
    """Photo model"""

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    source           = models.ImageField(upload_to=get_upload_to, blank=False, null=False, 
                            width_field='image_width', height_field='image_height')
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    display         = models.CharField(max_length=1, blank=True, null=True,
                            choices=DISPLAY_CHOICES, default='N')

    image_width     = models.IntegerField(editable=False, null=True)
    image_height    = models.IntegerField(editable=False, null=True)

    class Meta:
        app_label                = 'filizver'
        verbose_name            = _('Image')
        verbose_name_plural     = _('Images')

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        delete(self.source)
        super(Image, self).delete()


post_save.connect(add_entry_signal, sender=Image)
post_delete.connect(delete_entry_signal, sender=Image)

