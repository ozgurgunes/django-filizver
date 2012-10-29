# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

from filizver.topic.models import Topic
# from models import Entry
from plugins import EntryPoint

from djangoplugins.fields import PluginChoiceField


class EntryForm(forms.ModelForm):

    plugin      = PluginChoiceField(EntryPoint, widget=forms.HiddenInput)
            
