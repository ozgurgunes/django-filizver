# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Picture


class PictureAdmin(admin.ModelAdmin):
    list_display    = ('user', 'topic', 'date_created')
    list_filter     = ['date_created']
    search_fields   = ['caption']
    date_hierarchy  = 'date_created'

admin.site.register(Picture, PictureAdmin)
