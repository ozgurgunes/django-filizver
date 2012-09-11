# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from filizver.models import Topic
from filizver.forms import BranchForm
from filizver import views

urlpatterns = patterns('',
    url(r'^$', 
        views.TopicList.as_view(), 
        name='filizver_homepage'),
        
    url(r'^update/topic/(?P<id>\d+)/$',
        views.TopicUpdate.as_view(), 
        name='filizver_topic_update'),
        
    # url(r'^create/entry/(?P<id>\d+)/(?P<module>[-\w]+)$', 
    url(r'^create/entry/(?P<id>\d+)/$', 
        'filizver.views.entry_create', 
        name='filizver_entry_create'),    
        
    url(r'^sort/entries/(?P<id>\d+)/$', 
        views.entry_sort, 
        name='filizver_entry_sort'),    
        
    url(r'^delete/topic/(?P<pk>\d+)$', views.TopicDelete.as_view(), name='filizver_topic_delete'),

    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/(?P<id>\d+)/$', 
        views.TopicDetail.as_view(), 
        name='filizver_topic_detail'),
        
    url(r'^create/topic/$', 
        views.TopicCreate.as_view(), 
        name='filizver_topic_create'),    
        
    url(r'^delete/topic/complete/$', 
        TemplateView.as_view(template_name='filizver/topic_delete.html'), 
        name='filizver_topic_delete_complete'),
        
    url(r'^tags/$', 
        TemplateView.as_view(template_name='filizver/topic_tags.html'), 
        name='filizver_topic_tags'),
        
#    url(r'^tags/(?P<tag>.*)/$', views.topic_tagged, None, name='filizver_topic_tagged'),
#    url(r'^search/$', views.topic_search, None, name='filizver_topic_search'),
)
