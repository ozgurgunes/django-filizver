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
from django.db.models import Count

from manifest.accounts.views import LoginRequiredMixin
from filizver.core.views import ExtraContextMixin

from filizver.topic.models import Topic
from filizver.topic.forms import TopicForm
from filizver.entry.plugins import EntryType

class TopicList(ListView, ExtraContextMixin):

    queryset = Topic.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    

class TopicDetail(DetailView, ExtraContextMixin):

    queryset = Topic.objects.select_related().all()
    template_name = "topic/topic_detail.html"
    

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
        return reverse('filizver:topic_list')
