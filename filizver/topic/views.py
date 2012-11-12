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
from filizver.core.views import ExtraContextMixin, JSONResponseMixin

from models import Topic
from forms import TopicForm, ModeratorForm
from plugins import TopicPoint

class TopicList(ExtraContextMixin, ListView):

    queryset = Topic.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "topic/topic_list.html"
    extra_context = { 'topic_form': TopicForm() }
    

class TopicDetail(ExtraContextMixin, DetailView):

    queryset = Topic.objects.select_related(
                    'user__profile'
                ).prefetch_related('moderators', 'followers').all()
    template_name = "topic/topic_detail.html"
    extra_context = {
        'moderator_form': ModeratorForm()
    }


class TopicCreate(CreateView, LoginRequiredMixin):

    # form_class = TopicForm
    # template_name = "topic/topic_create.html"
    
    def get_form_class(self):
        if self.form_class:
            return self.form_class
        else:
            plugin  = TopicPoint.get_model(self.request.POST.get('plugin')).get_plugin()
            return plugin.form_class

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
        instance = form.save(commit=False)
        if instance.id:
            topic = instance.topic
        else:
            topic = Topic(user=self.request.user)
        topic.title = form.cleaned_data['title']
        topic.save()
        topic.plugins.add(self.plugin.get_model())
        instance.topic = topic
        instance.save()
        return redirect(instance.get_absolute_url())


class TopicUpdate(TopicCreate, UpdateView):
    pass


class TopicDelete(DeleteView, LoginRequiredMixin):

    model = Topic

    def get_success_url(self):
        return reverse('filizver:topic_list')

class TopicModerator(FormView, LoginRequiredMixin):

    model = Moderator

    def post(self, request, *args, **kwargs):
        pass
        
        
class TopicFollower(UpdateView, LoginRequiredMixin):

    model = Topic

    def post(self, request, *args, **kwargs):
        pass
        
        
