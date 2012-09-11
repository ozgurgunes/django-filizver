# -*- coding: utf-8 -*-
import settings
from django.views.generic import (View, ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve
from manifest.core.decorators import owner_required
from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.models import Topic, Entry
from filizver.forms import TopicForm, BranchForm, EntryForm, ImageForm, TextForm

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext


    
    
@login_required
def entry_create(request, id=None):
    topic = get_object_or_404(Topic, pk=id)

    if request.method == 'POST':
        POST = request.POST.copy()
        POST['user'] = request.user.id
        POST['topic'] = topic.id
        if POST['body_1']:
            POST['source_1'] = POST['body_1']
            form = BranchForm(POST)
            if form.is_valid():
                text = form.save()
                if request.is_ajax():
                    return HttpResponse('OK')
                return redirect(text.topic)        
            POST['source'] = POST['body_0']
            form = TextForm(POST)
            if form.is_valid():
                text = form.save()
                if request.is_ajax():
                    return HttpResponse('OK')
                return redirect(text.topic)        
        if request.FILES:
            form = ImageForm(POST, request.FILES)
            if form.is_valid():
                photo = form.save()
                if request.is_ajax():
                    image = request.FILES['source']
                    data = {
                        'id'    : photo.id, 
                        'name'  : image.name, 
                        'type'  : image.content_type, 
                        'size'  : image.size
                    }
                    return HttpResponse('['+simplejson.dumps(data)+']', mimetype='application/json')
                return redirect(photo.topic)
        form = EntryForm(initial={'user': request.user, 'topic': topic})
    else:
        form = EntryForm(initial={'user': request.user, 'topic': topic})
    extra_context = { 'topic': topic, 'form': form }
    return render_to_response('filizver/entry_create.html', extra_context, context_instance=RequestContext(request))

class TopicList(ListView):
    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_list.html"
            
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
    success_url = 'filizver_homepage'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.success_url)

class TopicUpdate(UpdateView, LoginRequiredMixin):
    model = Topic
    form_class = TopicForm
    template_name = "filizver/topic_update.html"
    success_url = '/topics'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    

class TopicDelete(DeleteView, LoginRequiredMixin):
    model = Topic
    #template_name = "filizver/topic_update.html"
    success_url = '/'
    #slug_field = 'id'
    #slug_url_kwarg = 'id'

@login_required
def entry_sort(request, id=None):
    topic = get_object_or_404(Topic, pk=id)
    if request.method == 'POST':
        for position, pk in enumerate(request.POST.getlist('entry[]')):
            Entry.objects.filter(pk=pk).update(position=position+1)
    extra_context = { 'object': topic }
    return render_to_response('filizver/_topic_entries.html', extra_context, context_instance=RequestContext(request))
