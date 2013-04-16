# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Text

class TextAdmin(admin.ModelAdmin):
    list_display = ['body','user','topic']
    
    
admin.site.register(Text, TextAdmin)