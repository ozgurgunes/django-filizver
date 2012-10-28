# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, ListView

from filizver.topic.forms import TopicForm

class ExtraContextMixin(View):
    """
    A mixin that passes ``extra_context`` dictionary as template context.
    
    """
    
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class AjaxResponseMixin(View):
    """
    A mixin that prefix the ``template_name`` with an underscore (_) if request is AJAX.
    
    """
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            folder, sep, file = self.template_name.rpartition('/')
            self.template_name = folder + sep + '_' + file
        return super(AjaxResponseMixin, self).dispatch(request, *args, **kwargs)
    

class Timeline(ListView, ExtraContextMixin):

    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Topic.objects.timeline(self.request.user).select_related()
        else:
            return Topic.objects.select_related().all()


