# -*- coding: utf-8 -*-
import settings
from django.views.generic import (View, ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve, reverse_lazy
from manifest.core.decorators import owner_required
from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.models import Topic, Entry
from filizver.forms import TopicForm, BranchForm, EntryForm

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext


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

    template_name = "filizver/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Topic.objects.timeline(self.request.user).select_related()
        else:
            return Topic.objects.select_related().all()


class TopicList(ListView, ExtraContextMixin):

    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    
    # def get_queryset(self):
    #     if self.request.user.is_authenticated():
    #         return Topic.objects.for_user(self.request.user).select_related()
    #     else:
    #         return Topic.objects.select_related().all()

            
class TopicDetail(DetailView):

    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_detail.html"
    extra_context = { 'entry_form': EntryForm() }

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
    
class TopicCreate(CreateView, LoginRequiredMixin):

    form_class = TopicForm
    template_name = "filizver/topic_create.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(instance.get_absolute_url())


class TopicUpdate(UpdateView, LoginRequiredMixin):

    model = Topic
    form_class = TopicForm
    template_name = "filizver/topic_update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class TopicDelete(DeleteView, LoginRequiredMixin):

    model = Topic

    def get_success_url(self):
        return reverse('filizver_homepage')


class EntryList(ListView):

    queryset = Entry.objects.select_related().all()
    template_name = "filizver/entry_list.html"


class EntryDetail(ListView):

    queryset = Entry.objects.select_related().all()
    template_name = "filizver/entry_list.html"


class EntryCreate(CreateView, LoginRequiredMixin):
    
    form_class = EntryForm
    template_name = "filizver/entry_create.html"
    
    def post(self, request, *args, **kwargs):
        POST = request.POST.copy()
        POST['user'] = request.user.id
        if POST['body_1']:
            POST['source_1'] = POST['body_1']
            form = BranchForm(POST)
            if form.is_valid():
                text = form.save()
                if request.is_ajax():
                    return HttpResponse('OK')
                return redirect(text.topic)        
        return HttpResponse('FAIL')

class EntryDelete(DeleteView, LoginRequiredMixin):

    model = Entry

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


class EntrySort(DetailView, UpdateView, LoginRequiredMixin):

    model = Topic
    template_name = 'filizver/_topic_entries.html'
    context = {}

    def post(self, request, *args, **kwargs):
        for position, pk in enumerate(request.POST.getlist('entry[]')):
            Entry.objects.filter(pk=pk).update(position=position+1)
        return super(EntrySort, self).post(request, *args, **kwargs)
