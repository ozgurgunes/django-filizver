# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Topic

from .plugins import TopicInline

TOPIC_INLINES = [plugin.admin() for plugin in TopicInline.get_plugins()]

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'plugins', ('user', 'moderators'), ('active', 'deleted', 'deleted_date'))
    read_only_fields = ('created_date', 'updated_date', 'deleted_date')
    raw_id_fields = ('user', 'moderators')
    inlines = TOPIC_INLINES


admin.site.register(Topic, TopicAdmin)
