# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filizver.models.text import Text


class TextForm(forms.ModelForm):
    class Meta:
        model       = Text
