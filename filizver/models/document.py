# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filizver.models.entry import AbstractEntry


class Document(AbstractEntry):
    """Photo model"""

    class Meta:
        verbose_name            = _('document')
        verbose_name_plural     = _('documents')

    def __unicode__(self):
        return u"%s" % self.source
