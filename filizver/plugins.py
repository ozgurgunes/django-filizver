# -*- coding: utf-8 -*-
from django.template.loader import select_template, render_to_string

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

        
class PluginPoint(object):
    __metaclass__ = PluginMount
    
    
class EntryPoint(PluginPoint):
    name = 'entry'
    title = 'Entry'

    template = None
    form_class = None
    
    @classmethod
    def get_template(self):
        #template = select_template(['filizver/%s_entry.html' % self.name, 'filizver/entry_list.html'])
        return self.template if self.template else 'filizver/%s_entry.html' % self.name
        
    @classmethod
    def render(self, context):
        return render_to_string(self.get_template(), context)

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


class PictureEntry(EntryPoint):    
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
