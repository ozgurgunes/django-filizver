# -*- coding: utf-8 -*-
from django.views.generic import (ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from manifest.core.decorators import owner_required
from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.models import Topic
from filizver.forms import TopicForm, BranchForm, PostForm

class TopicList(ListView):
    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_list.html"
            
class TopicDetail(DetailView):
    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_detail.html"
    extra_context = { 'branch_form': BranchForm() }

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
    template_name = "filizver/_topic_posts.html"
        
    
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

