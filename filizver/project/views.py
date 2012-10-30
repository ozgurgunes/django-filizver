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

from filizver.topic import views
from models import Project
from forms import ProjectForm
from plugins import ProjectTopic


class ProjectList(views.TopicList):

    queryset = Project.objects.select_related(
                    'topic__user__profile'
                ).all()
    template_name = "project/project_list.html"
    

class ProjectDetail(views.TopicDetail):

    queryset = Project.objects.select_related('topic__user__profile').all()
    template_name = "project/project_detail.html"
    

class ProjectCreate(views.TopicCreate):

    form_class = ProjectForm
    template_name = "project/project_form.html"
    plugin = ProjectTopic
    

class ProjectUpdate(views.TopicUpdate):

    model = Project
    form_class = ProjectForm
    template_name = "project/project_form.html"
    plugin = ProjectTopic


class ProjectDelete(views.TopicDelete):

    model = Project

    def get_success_url(self):
        return reverse('project:project_list')
