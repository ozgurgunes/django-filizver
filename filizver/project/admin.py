# coding: utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import Project

class ProjectInline(admin.StackedInline):
    model = Project
    raw_id_fields = ('moderators',)
    

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['topic',]
    raw_id_fields = ['moderators']

admin.site.register(Project, ProjectAdmin)
