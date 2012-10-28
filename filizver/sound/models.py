# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal
from filizver.core.utils import get_upload_to


class Sound(EntryBase):
    """Photo model"""

    source          = models.FileField(_('Source'), upload_to=get_upload_to, blank=True, null=True)
    url             = models.URLField(_('URL'), max_length=255, blank=True, null=True)
    embed           = models.TextField(_('Embed'), blank=True, null=True)
    title           = models.CharField(_('Title'), max_length=128, blank=True, null=True)
    description     = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        app_label                = 'filizver'
        verbose_name            = _('Sound')
        verbose_name_plural     = _('Sounds')

    def __unicode__(self):
        return u"%s" % self.source or self.url or self.embed

    def delete(self):
        try:
            delete(self.source)
        except:
            pass
        super(Sound, self).delete()


post_save.connect(add_entry_signal, sender=Sound)
post_delete.connect(delete_entry_signal, sender=Sound)

