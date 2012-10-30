# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',

    url(r'^$', 
        views.ProjectList.as_view(), 
        name='project_list'),
        
    url(r'^(?P<pk>\d+)/$', 
        views.ProjectDetail.as_view(), 
        name='project_detail'),
        
    url(r'^create/$', 
        views.ProjectCreate.as_view(), 
        name='project_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.ProjectUpdate.as_view(), 
        name='project_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.ProjectDelete.as_view(), 
        name='project_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(), 
        name='project_delete_complete'),
        
)
