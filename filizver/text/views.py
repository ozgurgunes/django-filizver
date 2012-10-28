# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)

from manifest.accounts.views import LoginRequiredMixin
from filizver.core.views import ExtraContextMixin, AjaxResponseMixin

from models import Text
from forms import TextForm


class TextList(ListView, ExtraContextMixin):

    queryset = Text.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "text/text_list.html"
    extra_context = { 'text_form': TextForm() }
    

class TextDetail(DetailView, ExtraContextMixin):

    queryset = Text.objects.select_related().all()
    template_name = "text/text_detail.html"


class TextCreate(CreateView, LoginRequiredMixin, AjaxResponseMixin):

    form_class = TextForm
    template_name = "text/text_form.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(instance.get_absolute_url())


class TextUpdate(UpdateView, LoginRequiredMixin):

    model = Text
    form_class = TextForm
    template_name = "text/text_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class TextDelete(DeleteView, LoginRequiredMixin):

    model = Text

    def get_success_url(self):
        return reverse('filizver:text_list')
