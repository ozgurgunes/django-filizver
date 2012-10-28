# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from filizver.topic.models import Topic
from filizver.text.models import Text

class TextForm(forms.ModelForm):
    body        = forms.CharField(widget=forms.Textarea(
                                    attrs={
                                        'class': 'title input', 
                                        'placeholder': _('Type your topic title')
                                    }))
    plugin      = forms.CharField(widget=forms.HiddenInput)
    
    class Meta:
        model       = Text
        fields = ['body','plugin']
        
    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)        
        self.fields['plugin'].initial = 'text'