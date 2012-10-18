# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Text


class TextForm(forms.ModelForm):
    source            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea markup', 'rows': 8, 'required': 'required'}))
#    footnote        = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Text
        exclude     = ['date_created', 'footnote']
        
class TextUpdateForm(forms.ModelForm):
    source          = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 8}))

    class Meta:
        model       = Text
        exclude     = ['date_created', 'footnote']
