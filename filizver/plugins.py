# -*- coding: utf-8 -*-


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
