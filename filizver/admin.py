# -*- coding: utf-8 -*-
from django.contrib import admin
from filizver.models import *

class BranchInline(admin.StackedInline):
    model                   =   Branch
    fk_name                 =   'source'

class EntryInline(admin.StackedInline):
    model                   =   Entry

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display    = ('title', 'user', 'date_created', 'is_public')
    list_filter     = ['date_created', 'is_public']
    search_fields   = ['title', 'description']
    date_hierarchy  = 'date_created'
    inlines         = [EntryInline, BranchInline]

class BranchAdmin(admin.ModelAdmin):
    list_display    = ('source', 'user', 'date_created')
        
class EntryAdmin(admin.ModelAdmin):
    list_display    = ('topic', 'user', 'content_type')
    sortable_field_name = 'position'

admin.site.register(Topic, TopicAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Entry, EntryAdmin)

class TextAdmin(admin.ModelAdmin):
    list_display    = ('user', 'topic', 'date_created')
    list_filter     = ['date_created']
    search_fields   = ['source']
    date_hierarchy  = 'date_created'

admin.site.register(Text, TextAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display    = ('user', 'topic', 'date_created')
    list_filter     = ['date_created']
    search_fields   = ['caption']
    date_hierarchy  = 'date_created'

admin.site.register(Image, ImageAdmin)
