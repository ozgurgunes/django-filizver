# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (View, ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve, reverse_lazy

from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.topic.models import Topic
from filizver.topic.forms import TopicForm
from filizver.entry.forms import EntryForm


class ExtraContextMixin(View):
    """
    A mixin that passes ``extra_context`` dictionary as template context.
    
    """
    
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class Timeline(ListView, ExtraContextMixin):

    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Topic.objects.timeline(self.request.user).select_related()
        else:
            return Topic.objects.select_related().all()


class TopicList(ListView, ExtraContextMixin):

    queryset = Topic.objects.select_related().all()
    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    
    # def get_queryset(self):
    #     if self.request.user.is_authenticated():
    #         return Topic.objects.for_user(self.request.user).select_related()
    #     else:
    #         return Topic.objects.select_related().all()

            
class TopicDetail(DetailView):

    queryset = Topic.objects.select_related().all()
    template_name = "topic/topic_detail.html"
    extra_context = { 'entry_form': EntryForm() }

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
    
class TopicCreate(CreateView, LoginRequiredMixin):

    form_class = TopicForm
    template_name = "topic/topic_create.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(instance.get_absolute_url())


class TopicUpdate(UpdateView, LoginRequiredMixin):

    model = Topic
    form_class = TopicForm
    template_name = "topic/topic_update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class TopicDelete(DeleteView, LoginRequiredMixin):

    model = Topic

    def get_success_url(self):
        return reverse('filizver_homepage')

