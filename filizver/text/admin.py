# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Text

class TextAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Text, TextAdmin)