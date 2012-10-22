# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from filizver.entry import views


urlpatterns = patterns('',

    url(r'^create/(?P<pk>\d+)/$', 
        views.EntryCreate.as_view(),
        name='entry_create'),    
        
    url(r'^delete/(?P<pk>\d+)/$', 
        views.EntryDelete.as_view(),
        name='entry_delete'),    

    url(r'^sort/(?P<pk>\d+)/$', 
        views.EntrySort.as_view(), 
        name='entry_sort'),    
        
)
