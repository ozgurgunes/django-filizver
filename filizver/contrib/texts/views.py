# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.utils import simplejson
from django.http import HttpResponse
from manifest.accounts.views import LoginRequiredMixin


class ImageCreate(CreateView, LoginRequiredMixin):
    
    form_class = ImageForm
    template_name = "filizver/image_create.html"
    
    def post(self, request, *args, **kwargs):
        if request.POST['body_0']:
            form = TextForm(request.POST)
            if form.is_valid():
                text = form.save()
                if request.is_ajax():
                    return HttpResponse('OK')
                return redirect(text.topic)        
        return HttpResponse('FAIL')
