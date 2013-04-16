# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views


urlpatterns = patterns('',

    url(r'^$', 
        views.ImageList.as_view(), 
        name='image_list'),
        
    url(r'^(?P<id>\d+)/$', 
        views.ImageDetail.as_view(), 
        name='image_detail'),
        
    url(r'^create/$', 
        views.ImageCreate.as_view(), 
        name='image_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.ImageUpdate.as_view(), 
        name='image_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.ImageDelete.as_view(), 
        name='image_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(template_name='image/image_delete_complete.html'), 
        name='image_delete_complete'),
        
)
