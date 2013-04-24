# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filizver.models import Topic, Moderator, Text, Image, Link, Document, Video, Sound


class TopicFormBase(forms.ModelForm):
    
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))

    class Meta:
        model = Topic
    
    def get_ip_address(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class TopicForm(forms.ModelForm):
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))
    class Meta:
        model       = Topic
        exclude     = ['user', 'slug', 'branches', 'tags', 'created_date', 'is_public']
        fields = ['title', 'body', 'image','plugin']


class ModeratorForm(forms.ModelForm):
    
    class Meta:
        model       = Moderator
        fields      = ['user','topic']


class TextForm(forms.ModelForm):
    
    class Meta:
        model       = Text
        fields      = ['user','topic']

class ImageForm(forms.ModelForm):
    
    class Meta:
        model       = Image
        fields      = ['user','topic']

class LinkForm(forms.ModelForm):
    
    class Meta:
        model       = Link
        fields      = ['user','topic']


class DocumentForm(forms.ModelForm):
    
    class Meta:
        model       = Document
        fields      = ['user','topic']

class VideoForm(forms.ModelForm):
    
    class Meta:
        model       = Video
        fields      = ['user','topic']

class SoundForm(forms.ModelForm):
    
    class Meta:
        model       = Sound
        fields      = ['user','topic']
