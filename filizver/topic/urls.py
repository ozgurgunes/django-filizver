# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',

    url(r'^$', 
        views.TopicList.as_view(), 
        name='topic_list'),
        
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/(?P<id>\d+)/$', 
        views.TopicDetail.as_view(), 
        name='topic_detail'),
        
    url(r'^create/$', 
        views.TopicCreate.as_view(), 
        name='topic_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.TopicUpdate.as_view(), 
        name='topic_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.TopicDelete.as_view(), 
        name='topic_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(template_name='topic/topic_delete.html'), 
        name='topic_delete_complete'),
        
    # url(r'^tags/$', 
    #     TemplateView.as_view(template_name='topic/topic_tags.html'), 
    #     name='topic_tags'),
        
    # url(r'^tags/(?P<tag>.*)/$', views.topic_tagged, None, name='filizver_topic_tagged'),

)
