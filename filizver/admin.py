# -*- coding: utf-8 -*-
from django.contrib import admin
from filizver.models import Topic


class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', ('user', 'created_date'), 
                ('updated_date', 'updated_user'), 
                ('deleted_date', 'deleted_user'))
    readonly_fields = ('user','created_date', 'updated_date', 'deleted_date', 'updated_user', 'deleted_user')
    raw_id_fields = ('user', 'moderators')


admin.site.register(Topic, TopicAdmin)
