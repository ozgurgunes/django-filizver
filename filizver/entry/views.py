# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (View, ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

from manifest.accounts.views import LoginRequiredMixin

from filizver.topic.models import Topic
from filizver.entry.models import Entry
from filizver.topic.forms import TopicForm
from filizver.entry.forms import EntryForm
from filizver.branch.forms import BranchForm



class EntryList(ListView):

    queryset = Entry.objects.select_related().all()
    template_name = "entry/_tntry_list.html"


class EntryDetail(ListView):

    queryset = Entry.objects.select_related().all()
    template_name = "entry/_tntry_list.html"


class EntryCreate(CreateView, LoginRequiredMixin):
    
    form_class = EntryForm
    template_name = "entry/_tntry_create.html"
    
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
    template_name = 'topic/_topic_entries.html'
    context = {}

    def post(self, request, *args, **kwargs):
        for position, pk in enumerate(request.POST.getlist('entry[]')):
            Entry.objects.filter(pk=pk).update(position=position+1)
        return super(EntrySort, self).post(request, *args, **kwargs)
