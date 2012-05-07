from django.contrib import admin
from filizver.models import *

class BranchInline(admin.StackedInline):
    model                   =   Branch
    fk_name                 =   'source'

class PostInline(admin.StackedInline):
    model                   =   Post

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display    = ('title', 'user', 'date_created', 'is_public')
    list_filter     = ['date_created', 'is_public']
    search_fields   = ['title', 'description']
    date_hierarchy  = 'date_created'
    inlines         = [PostInline, BranchInline]

class BranchAdmin(admin.ModelAdmin):
    list_display    = ('source', 'user', 'date_created')
        
class PostAdmin(admin.ModelAdmin):
    list_display    = ('topic', 'user', 'content_type')
    sortable_field_name = 'position'

admin.site.register(Topic, TopicAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Post, PostAdmin)
