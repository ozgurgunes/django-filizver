from django.contrib import admin
from filizver.contrib.passages.models import *

class PassageAdmin(admin.ModelAdmin):
    list_display    = ('user', 'topic', 'date_created')
    list_filter     = ['date_created']
    search_fields   = ['body']
    date_hierarchy  = 'date_created'

admin.site.register(Passage, PassageAdmin)
