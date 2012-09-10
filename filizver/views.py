# -*- coding: utf-8 -*-
import settings
from django.views.generic import (ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from manifest.core.decorators import owner_required
from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.models import Topic
from filizver.forms import TopicForm, BranchForm, EntryForm, ImageForm, TextForm

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext


@login_required
def entry_create(request, id=None):
    topic = get_object_or_404(Topic, pk=id)

    if request.method == 'POST':
        # POST = request.POST.copy()
        # FILES = request.FILES.copy()
        # POST['user'] = request.user.id
        # POST['topic'] = topic.id
        # if POST['branch_1']:
        #     POST['source_1'] = POST['branch_1']
        #     form = BranchForm(POST)
        #     if form.is_valid():
        #         text = form.save()
        #         if request.is_ajax():
        #             return HttpResponse('OK')
        #         return redirect(text.topic)        
        # if POST['text']:
        #     POST['source'] = POST['text']
        #     form = TextForm(POST)
        #     if form.is_valid():
        #         text = form.save()
        #         if request.is_ajax():
        #             return HttpResponse('OK')
        #         return redirect(text.topic)        
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            if request.is_ajax():
                image = request.FILES['image']
                data = {
                    'id'    : photo.id, 
                    'name'  : image.name, 
                    'type'  : image.content_type, 
                    'size'  : image.size
                }
                return HttpResponse(simplejson.dumps(data), mimetype='application/json')
            return redirect(photo.topic)
    
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
    form_class = TopicForm
    template_name = "filizver/topic_update.html"
    success_url = '/topics'
    

class TopicSort(TopicDetail, LoginRequiredMixin):
    template_name = "filizver/_topic_entries.html"
        
    
class TopicFormView(FormView, LoginRequiredMixin):
    form_class = TopicForm
    template_name = "filizver/topic_form.html"
    success_url = '/topics'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        try: 
            instance.user
        except ObjectDoesNotExist:
            instance.user = self.request.user
        instance.save()
        return redirect(self.success_url)

