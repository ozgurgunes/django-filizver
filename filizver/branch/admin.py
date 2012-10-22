# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Branch


class BranchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Branch, BranchAdmin)
