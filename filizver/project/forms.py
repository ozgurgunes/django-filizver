# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

from filizver.topic.forms import TopicFormBase
from models import Project

class ProjectForm(TopicFormBase):
    class Meta:
        model = Project
        fields = ['description']