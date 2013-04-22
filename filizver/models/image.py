# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filizver.models.entry import AbstractEntry


class Image(AbstractEntry):
    """Photo model"""

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    
    alt             = models.CharField(max_length=128, blank=True, null=True)
    caption         = models.TextField(blank=True, null=True)

    display         = models.CharField(max_length=1, blank=True, null=True,
                            choices=DISPLAY_CHOICES, default='N')


    class Meta:
        verbose_name            = _('image')
        verbose_name_plural     = _('images')

    def __unicode__(self):
        return u"%s" % self.image

