# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

from filizver.topic.models import Topic

class TopicFormBase(forms.ModelForm):
    
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))

    class Meta:
        model = Topic
        
    def __init__(self, *args, **kw):
        super(TopicFormBase, self).__init__(*args, **kw)
        new_order = self.fields.keyOrder[:-1]
        new_order.insert(0, 'title')
        self.fields.keyOrder = new_order
        try:
            self.fields['title'].initial = self.instance.topic.title
        except:
            pass

    def save(self, force_insert=False, force_update=False, commit=False):
        instance = super(TopicFormBase, self).save(commit=commit)
        if instance.id:
            topic = instance.topic
        else:
            topic = Topic(user=instance.user)
        topic.title = self.cleaned_data['title']
        topic.save()
        instance.topic = topic
        instance.save()
        return instance


class TopicForm(forms.ModelForm):
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))
    class Meta:
        model       = Topic
        exclude     = ['user', 'slug', 'branches', 'tags', 'created_date', 'is_public']
