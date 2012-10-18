# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, CreateView
from filizver.models import Topic
from filizver.contrib.pictures.models import Picture
from filizver.contrib.pictures.forms import PictureForm
from filizver.contrib.pictures.plugins import PictureTopic


urlpatterns = patterns('',

    url(r'^create/$', 
        CreateView.as_view(model=Topic, form_class=PictureTopic.form_class), 
        name='filizver_picture_create'),
        
)
