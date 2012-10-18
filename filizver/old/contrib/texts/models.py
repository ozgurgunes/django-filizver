# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.models import EntryBase, add_entry_signal, delete_entry_signal


class Text(EntryBase):
    """Passage model"""

    source            = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name            = _('Text')
        verbose_name_plural     = _('Texts')

    def __unicode__(self):
        return u"%s" % self.source
        

post_save.connect(add_entry_signal, sender=Text)
post_delete.connect(delete_entry_signal, sender=Text)        
