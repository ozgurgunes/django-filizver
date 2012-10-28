# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views


urlpatterns = patterns('',

    url(r'^$', 
        views.BranchList.as_view(), 
        name='branch_list'),
        
    url(r'^(?P<id>\d+)/$', 
        views.BranchDetail.as_view(), 
        name='branch_detail'),
        
    url(r'^create/$', 
        views.BranchCreate.as_view(), 
        name='branch_create'),    
        
    url(r'^update/(?P<pk>\d+)/$',
        views.BranchUpdate.as_view(), 
        name='branch_update'),
        
    url(r'^delete/(?P<pk>\d+)$', 
        views.BranchDelete.as_view(), 
        name='branch_delete'),

    url(r'^delete/complete/$', 
        TemplateView.as_view(template_name='branch/branch_delete_complete.html'), 
        name='branch_delete_complete'),
        
)
