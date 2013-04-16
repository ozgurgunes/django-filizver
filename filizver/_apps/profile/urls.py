# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from filizver.topic.models import Topic
from filizver.profile.models import Profile
from filizver.profile.forms import ProfileForm


urlpatterns = patterns('',

    url(r'^$', 
        ListView.as_view(model=Profile),
        name='profile_list'),
        
    url(r'^create/$', 
        CreateView.as_view(model=Profile, form_class=ProfileForm),
        name='profile_create'),    
        
    url(r'^(?P<username>[-\w]+)/$', 
        DetailView.as_view(model=Profile, slug_field='user__username', slug_url_kwarg='username'),
        name='profile_detail'),
        
    url(r'^update/(?P<pk>\d+)/$',
        UpdateView.as_view(model=Profile, form_class=ProfileForm),
        name='profile_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        DeleteView.as_view(model=Profile),
        name='profile_delete'),
        
)
