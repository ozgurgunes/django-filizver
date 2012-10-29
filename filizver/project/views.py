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

from filizver.project.models import Project
from filizver.project.forms import ProjectForm
from filizver.entry.plugins import EntryPoint


class ProjectList(ListView, ExtraContextMixin):

    queryset = Project.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "project/project_list.html"
    

class ProjectDetail(DetailView, ExtraContextMixin):

    queryset = Project.objects.select_related().all()
    template_name = "project/project_detail.html"
    

