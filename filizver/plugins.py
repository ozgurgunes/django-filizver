# -*- coding: utf-8 -*-
from djangoplugins.point import PluginPoint


class EntryPoint(PluginPoint):

    form_class = None
    
    def create(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.topic_id = request.POST.get('topic')
            obj.save()
            if request.is_ajax():
                return HttpResponse('OK')
            return obj

class UserEntry(EntryPoint):

    name = 'user'
    title = 'User'


class TextEntry(EntryPoint):

    name = 'text'
    title = 'Text'


class ImageEntry(EntryPoint):
    
    name = 'image'
    title = 'Image'

    def create(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            if request.is_ajax():
                picture = request.FILES['source']
                data = {
                    'id'    : obj.id, 
                    'name'  : picture.name, 
                    'type'  : picture.content_type, 
                    'size'  : picture.size
                }
                return HttpResponse('['+json.dumps(data)+']', mimetype='application/json')
            return redirect(obj.topic)        


class LinkEntry(EntryPoint):
    name = 'link'
    title = 'Link'


class DocumentEntry(EntryPoint):
    name = 'document'
    title = 'Document'


class VideoEntry(EntryPoint):
    name = 'video'
    title = 'Video'

class SoundEntry(EntryPoint):
    name = 'sound'
    title = 'Sound'
