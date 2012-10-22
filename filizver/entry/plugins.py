# -*- coding: utf-8 -*-
from djangoplugins.point import PluginPoint


class EntryType(PluginPoint):
    
    form_class = None
    
    def get_form(self, request, topic, *args, **kwargs):
        return self.form_class(request.POST, request.FILES, *args, **kwargs)
        
    def render(self, template, context):
        pass

