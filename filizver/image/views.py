# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)

from manifest.accounts.views import LoginRequiredMixin
from filizver.core.views import ExtraContextMixin, AjaxResponseMixin

from models import Image
from forms import ImageForm


class ImageList(ListView, ExtraContextMixin):

    queryset = Image.objects.select_related(
                    'user__profile'
                ).all()
    template_name = "image/image_list.html"
    extra_conimage = { 'image_form': ImageForm() }
    

class ImageDetail(DetailView, ExtraContextMixin):

    queryset = Image.objects.select_related().all()
    template_name = "image/image_detail.html"


class ImageCreate(CreateView, LoginRequiredMixin, AjaxResponseMixin):

    form_class = ImageForm
    template_name = "image/image_form.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(instance.get_absolute_url())


class ImageUpdate(UpdateView, LoginRequiredMixin):

    model = Image
    form_class = ImageForm
    template_name = "image/image_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ImageDelete(DeleteView, LoginRequiredMixin):

    model = Image

    def get_success_url(self):
        return reverse('filizver:image_list')
