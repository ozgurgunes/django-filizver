# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.image import ImageForm


class ImageEntry(EntryPoint):
    
    name = 'image'
    title = 'Image'
    form_class = ImageForm
    link = reverse('filizver:image_create')

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
