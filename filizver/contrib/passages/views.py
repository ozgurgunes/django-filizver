# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.models import User
from filizver.contrib.passages.models import Passage
from filizver.models import Topic
from filizver.contrib.passages.forms import PassageForm, PassageUpdateForm
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest

@login_required
def passage_create(request, topic_id=None):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = PassageForm(request.POST)
        if form.is_valid():
            passage = form.save()
            if request.is_ajax():
                return HttpResponse('OK')
            return redirect(passage.topic)
    else:
        form = PassageForm(initial={'user': request.user, 'topic': topic})
    template_name = 'passages/passage_create_ajax.html' if request.is_ajax() else 'passages/passage_create.html'
    extra_context={'form': form, 'topic': topic}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))

def passage_update(request, id=None):
    passage = get_object_or_404(Passage, pk=id)
    if request.method == 'POST':
        form = PassageForm(request.POST, instance=passage)
        if form.is_valid():
            passage = form.save()
            if request.is_ajax():
                return HttpResponse('OK')
            return redirect(passage.topic)
    else:
        form = PassageForm(instance=passage)
    template_name = 'passages/passage_update_ajax.html' if request.is_ajax() else 'passages/passage_update.html'
    extra_context={'form': form, 'object': passage}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))

def passage_delete(request, id=None):
    passage = get_object_or_404(Passage, pk=id)
    if request.method == 'POST':
        topic = passage.topic
        passage.delete()
        if request.is_ajax():
            return HttpResponse('OK')
        return redirect(topic)
    template_name = 'passages/passage_delete_ajax.html' if request.is_ajax() else 'passages/passage_delete.html'
    extra_context={'object': passage}
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))
