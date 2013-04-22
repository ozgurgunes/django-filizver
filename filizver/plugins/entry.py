# -*- coding: utf-8 -*-
from djangoplugins.point import PluginPoint


class EntryPoint(PluginPoint):

    form_class = None
    
    def create(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.topic_id = request.POST.get('topic')
            obj.save()
            if request.is_ajax():
                return HttpResponse('OK')
            return obj
