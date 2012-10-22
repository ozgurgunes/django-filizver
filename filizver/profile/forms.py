# -*- coding: utf-8 -*-
from django import forms

from filizver.topic.forms import TopicFormBase
from filizver.profile.models import Profile

class ProfileForm(TopicFormBase):
    class Meta:
        model = Profile
