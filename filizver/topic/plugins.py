# -*- coding: utf-8 -*-
from djangoplugins.point import PluginPoint
from django.core import serializers

class TopicPoint(PluginPoint):

    form_class = None

    def create(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            if request.is_ajax():
                return HttpResponse(serializers.serialize('json', obj))
            return obj


class TopicInline(PluginPoint):

    def admin(self):
        return self.inline
