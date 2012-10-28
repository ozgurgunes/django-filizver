# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal
from filizver.core.utils import get_upload_to


class Document(EntryBase):
    """Photo model"""

    source          = models.FileField(upload_to=get_upload_to, blank=False, null=False)
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    class Meta:
        app_label                = 'filizver'
        verbose_name            = _('Document')
        verbose_name_plural     = _('Documents')

    def __unicode__(self):
        return u"%s" % self.source

    def delete(self):
        delete(self.source)
        super(Document, self).delete()


post_save.connect(add_entry_signal, sender=Document)
post_delete.connect(delete_entry_signal, sender=Document)

