# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',

    url(r'^$', 
        views.BoardList.as_view(), 
        name='board_list'),
        
    url(r'^(?P<pk>\d+)/$', 
        views.BoardDetail.as_view(), 
        name='board_detail'),
        
    url(r'^create/$', 
        views.BoardCreate.as_view(), 
        name='board_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.BoardUpdate.as_view(), 
        name='board_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.BoardDelete.as_view(), 
        name='board_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(), 
        name='board_delete_complete'),
        
)
