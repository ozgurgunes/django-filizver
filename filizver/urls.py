# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
 
    url(r'^topic/', include('filizver.topic.urls')),
    url(r'^entry/', include('filizver.entry.urls')),
    #url(r'^branch/', include('filizver.branch.urls')),
    #url(r'^text/', include('filizver.text.urls')),
    #url(r'^link/', include('filizver.link.urls')),   

)