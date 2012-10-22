# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Picture

class PictureAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Picture, PictureAdmin)