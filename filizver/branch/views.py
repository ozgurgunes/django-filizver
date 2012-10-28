# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)

from manifest.accounts.views import LoginRequiredMixin
from filizver.core.views import ExtraContextMixin, AjaxResponseMixin

from models import Branch
from forms import BranchForm


class BranchList(ListView, ExtraContextMixin):

    queryset = Branch.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "branch/branch_list.html"
    extra_conbranch = { 'branch_form': BranchForm() }
    

class BranchDetail(DetailView, ExtraContextMixin):

    queryset = Branch.objects.select_related().all()
    template_name = "branch/branch_detail.html"


class BranchCreate(CreateView, LoginRequiredMixin, AjaxResponseMixin):

    form_class = BranchForm
    template_name = "branch/branch_form.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(instance.get_absolute_url())


class BranchUpdate(UpdateView, LoginRequiredMixin):

    model = Branch
    form_class = BranchForm
    template_name = "branch/branch_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class BranchDelete(DeleteView, LoginRequiredMixin):

    model = Branch

    def get_success_url(self):
        return reverse('filizver:branch_list')
