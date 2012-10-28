# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views


urlpatterns = patterns('',

    url(r'^$', 
        views.TextList.as_view(), 
        name='text_list'),
        
    url(r'^(?P<id>\d+)/$', 
        views.TextDetail.as_view(), 
        name='text_detail'),
        
    url(r'^create/$', 
        views.TextCreate.as_view(), 
        name='text_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.TextUpdate.as_view(), 
        name='text_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.TextDelete.as_view(), 
        name='text_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(template_name='text/text_delete_complete.html'), 
        name='text_delete_complete'),
        
)
