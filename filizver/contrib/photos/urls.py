# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from filizver.contrib.photos.models import *
from filizver.contrib.photos import views

list_dict = {
    'queryset': Photo.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^(?P<id>\d+)/$',
        view='object_detail',
        kwargs=list_dict,
        name='photos_photo_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=list_dict,
        name='photos_photo_list',
    ),
)

urlpatterns += patterns('',
    url(r'^create/photo/(?P<topic_id>\d+)/$', views.photo_create, name='photos_photo_create'),    
    url(r'^update/photo/(?P<id>\d+)/$', views.photo_update, name='photos_photo_update'),
    url(r'^delete/photo/(?P<id>\d+)/$', views.photo_delete, name='photos_photo_delete'),
    url(r'^display/photo/(?P<id>\d+)/$', views.photo_display, name='photos_photo_display'),
)
