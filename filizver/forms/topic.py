# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filizver.models.topic import Topic, Moderator


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

    # def save(self, commit=True, *args, **kwargs):
    #     instance = super(TopicFormBase, self).save(commit=False)
    #     if instance.id:
    #         topic = instance.topic
    #     else:
    #         topic = Topic(user=self.instance.user)
    #     topic.title = self.cleaned_data['title']
    #     topic.save()
    #     instance.topic = topic
    #     instance.save(commit=commit)
    #     return instance


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
