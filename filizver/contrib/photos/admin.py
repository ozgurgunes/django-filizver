from django.contrib import admin
from filizver.contrib.photos.models import *

class PhotoAdmin(admin.ModelAdmin):
    list_display    = ('user', 'topic', 'date_created')
    list_filter     = ['date_created']
    search_fields   = ['caption']
    date_hierarchy  = 'date_created'

admin.site.register(Photo, PhotoAdmin)
