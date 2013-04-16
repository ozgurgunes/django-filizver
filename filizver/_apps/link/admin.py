# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Link

class LinkAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Link, LinkAdmin)