# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.utils import simplejson
from django.http import HttpResponse
from manifest.accounts.views import LoginRequiredMixin


class PictureCreate(CreateView, LoginRequiredMixin):
    
    form_class = PictureForm
    template_name = "filizver/picture_create.html"
    
    def post(self, request, *args, **kwargs):
        if request.FILES:
            form = PictureForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save()
                if request.is_ajax():
                    picture = request.FILES['source']
                    data = {
                        'id'    : photo.id, 
                        'name'  : picture.name, 
                        'type'  : picture.content_type, 
                        'size'  : picture.size
                    }
                    return HttpResponse('['+simplejson.dumps(data)+']', mimetype='application/json')
                return redirect(photo.topic)
        return HttpResponse('FAIL')
