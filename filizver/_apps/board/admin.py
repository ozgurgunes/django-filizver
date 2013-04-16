# coding: utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import Board

class BoardInline(admin.StackedInline):
    model = Board
    raw_id_fields = ('moderators',)
    

class BoardAdmin(admin.ModelAdmin):
    list_display = ['topic',]
    raw_id_fields = ['moderators']

admin.site.register(Board, BoardAdmin)
