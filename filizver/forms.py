# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from filizver.models import Topic, Post, Branch
from filizver.lookups import BranchLookup
from selectable.forms.widgets import AutoCompleteSelectWidget

class TopicForm(forms.ModelForm):
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))
    class Meta:
        model       = Topic
        exclude     = ['user', 'slug', 'branches', 'tags', 'date_created', 'is_public']

class PostForm(forms.ModelForm):
    topic           = forms.ModelChoiceField(queryset=Post.objects.all(), widget=forms.HiddenInput)
    
    class Meta:
        model       = Post
        exclude     = ['content_type', 'object_id', 'content_object', 'date_created', 'position']

class BranchForm(forms.ModelForm):
    topic           = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput)
    #source          = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.TextInput(attrs={ 'class': 'branch text' }))
    source          = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=AutoCompleteSelectWidget(BranchLookup, attrs={'placeholder': _('Branch out')}))

    class Meta:
        model       = Branch
        exclude     = ['user','date_created']
