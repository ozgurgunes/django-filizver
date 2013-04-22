# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filizver.models.entry import AbstractEntry


class Video(AbstractEntry):

    embed           = models.TextField(_('Embed'), blank=True, null=True)

    class Meta:
        verbose_name            = _('video')
        verbose_name_plural     = _('videos')

    def __unicode__(self):
        return u"%s" % self.file or self.url or self.embed
