# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views


urlpatterns = patterns('',

    url(r'^$', 
        views.TopicList.as_view(template_name='project/project_list.html'), 
        name='project_list'),
        
    url(r'^(?P<id>\d+)/$', 
        views.TopicDetail.as_view(template_name='project/project_detail.html'), 
        name='project_detail'),
        
    url(r'^create/$', 
        views.TopicCreate.as_view(template_name='project/project_form.html'), 
        name='project_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.TopicUpdate.as_view(template_name='project/project_form.html'), 
        name='project_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.TopicDelete.as_view(template_name='project/project_delete.html'), 
        name='project_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(template_name='project/project_delete_complete.html'), 
        name='project_delete_complete'),
        
)
