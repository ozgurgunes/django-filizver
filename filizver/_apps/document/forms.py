# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from filizver.topic.models import Topic
from models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model       = Document
        fields = ['source','title']
