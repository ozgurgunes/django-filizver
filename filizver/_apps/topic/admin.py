# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Topic

from .plugins import TopicPoint

TOPIC_INLINES = [plugin.admin() for plugin in TopicPoint.get_plugins()]

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'active', 
                ('user', 'created_date'), 
                ('updated_date', 'updated_user'), 
                ('deleted_date', 'deleted_user'),
                'plugins')
    readonly_fields = ('user','created_date', 'updated_date', 'deleted_date', 'updated_user', 'deleted_user')
    raw_id_fields = ('user', 'moderators')
    inlines = TOPIC_INLINES


admin.site.register(Topic, TopicAdmin)
