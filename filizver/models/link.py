# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filizver.models.entry import AbstractEntry


class Link(AbstractEntry):
    
    class Meta:
        verbose_name            = _('link')
        verbose_name_plural     = _('links')

    def __unicode__(self):
        return u"%s" % self.url
