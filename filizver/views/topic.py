# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView, FormView, CreateView,
                                    UpdateView, DeleteView)

from manifest.accounts.views import LoginRequiredMixin
from filizver.views.core import ExtraContextMixin, JSONResponseMixin

from filizver.models import Topic, Moderator
from filizver.forms import TopicForm, ModeratorForm

class Index(ExtraContextMixin, ListView):

    queryset = Topic.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    

class Topic(ExtraContextMixin, DetailView):

    queryset = Topic.objects.select_related(
                    'user__profile'
                ).prefetch_related('moderators', 'followers').all()
    template_name = "topic/topic_detail.html"
    extra_context = {
        'moderator_form': ModeratorForm()
    }


class Create(CreateView, LoginRequiredMixin):

    form_class = TopicForm
    template_name = "topic/topic_create.html"
    

    def get_ip_address(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    # def post(self, request, *args, **kwargs):
    #     plugin  = TopicPoint.get_model(request.POST.get('plugin')).get_plugin()
    #     topic   = plugin.create(request)
    #     return redirect(topic)
    
    def form_valid(self, form):
        topic = form.save(commit=False)
        if not topic.id:
            topic.user = self.request.user
        #topic.title = form.cleaned_data['title']
        topic.save()
        return redirect(topic.get_absolute_url())


class Update(TopicCreate, UpdateView):
    model = Topic
    template_name = "topic/topic_update.html"


class Delete(DeleteView, LoginRequiredMixin):

    model = Topic

    def get_success_url(self):
        return reverse('filizver:topic_list')



class Rating(FormView, LoginRequiredMixin):

    model = Rating

    def post(self, request, *args, **kwargs):
        pass
        
        

class Moderator(FormView, LoginRequiredMixin):

    model = Moderator

    def post(self, request, *args, **kwargs):
        pass
        
        

class Follower(UpdateView, LoginRequiredMixin):

    model = Follower

    def post(self, request, *args, **kwargs):
        pass
        
