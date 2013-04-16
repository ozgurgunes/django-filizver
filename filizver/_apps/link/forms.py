# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from filizver.topic.models import Topic
from models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model       = Link
        fields = ['url','title']
