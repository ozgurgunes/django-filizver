# -*- coding: utf-8 -*-
import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from filizver.contrib.photos.models import Photo
from filizver.models import Topic

class PhotoForm(forms.ModelForm):
    user            = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    topic          = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput())
    image           = forms.ImageField()

    class Meta:
        model       = Photo
        exclude     = ['date_created', 'title', 'description', 'image_width', 'image_height']
        
    class Media:
        js          = (settings.STATIC_URL + 'js/photo.upload.js',)
        
    def clean_image(self):
        from StringIO import StringIO  
        from PIL import Image

        if self.cleaned_data.get('image'):
            image_data = self.cleaned_data['image']
            if 'error' in image_data:
                raise forms.ValidationError(_('Upload a valid image. The file you uploaded was either not an image or a corrupted image.'))
                
            content_type = image_data.content_type
            if content_type:
                main, sub = content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                    raise forms.ValidationError(_('JPEG, PNG or GIF only.'))
        
            if image_data.size > 1024 * 1024 * 2:
                raise forms.ValidationError(_('Image size too big, max allowed size is 2MB'))
            """
            x, y = Image.open(image_data.temporary_file_path()).size
            if y < 128 or x < 128:  
                raise forms.ValidationError(_('Upload a valid image. This one is too small in size.'))  
            """            
            return self.cleaned_data['image']

class PhotoUpdateForm(forms.ModelForm):
    title               = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'class': 'title text' }))
    description         = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Photo
        fields      = ['title', 'description']
        exclude     = ['date_created', 'image', 'image_width', 'image_height']
