# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.models import User
from filizver.contrib.photos.models import Photo
from filizver.models import Topic
from filizver.contrib.photos.forms import PhotoForm, PhotoUpdateForm
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest

@login_required
def photo_create(request, topic_id=None):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            if request.is_ajax():
                update_form = PhotoUpdateForm(instance=photo)
                image = request.FILES['image']
                data = {
                    'update_form': render_to_string('photos/_photo_update_form.html', 
                        { 'object' : photo, 'form': update_form }, context_instance=RequestContext(request)), 
                    'id'    : photo.id, 
                    'name'  : image.name, 
                    'type'  : image.content_type, 
                    'size'  : image.size
                }
                return HttpResponse(simplejson.dumps(data), mimetype='application/json')
            return redirect(photo.topic)
    else:
        form = PhotoForm(initial={'user': request.user, 'topic': topic})
    template_name = 'photos/photo_create_ajax.html' if request.is_ajax() else 'photos/photo_create.html'
    extra_context={'form': form, 'topic': topic}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))

def photo_update(request, id=None):
    photo = get_object_or_404(Photo, pk=id)
    if request.method == 'POST':
        form = PhotoUpdateForm(request.POST, instance=photo)
        if form.is_valid():
            photo = form.save()
            if request.is_ajax():
                return HttpResponse('OK')
            return redirect(photo.topic)
    else:
        form = PhotoUpdateForm(instance=photo)
    template_name = 'photos/photo_update_ajax.html' if request.is_ajax() else 'photos/photo_update.html'
    extra_context={'form': form, 'object': photo}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))

def photo_delete(request, id=None):
    photo = get_object_or_404(Photo, pk=id)
    if request.method == 'POST':
        topic = photo.topic
        photo.delete()
        if request.is_ajax():
            return HttpResponse('OK')
        return redirect(topic)
    template_name = 'photos/photo_delete_ajax.html' if request.is_ajax() else 'photos/photo_delete.html'
    extra_context={'object': photo}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))

def photo_display(request, id=None):
    photo = get_object_or_404(Photo, pk=id)
    if request.method == 'POST':
        if request.POST.get('display') in ['L', 'N', 'R']:
            photo.display = request.POST.get('display') 
            photo.save()
            #return redirect(photo.topic)
    extra_context = { 'object': photo.topic }
    return render_to_response('filizver/_topic_posts.html', extra_context, context_instance=RequestContext(request))
