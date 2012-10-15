# -*- coding: utf-8 -*-
from StringIO import StringIO  
from PIL import Image

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from models import Picture


class PictureForm(forms.ModelForm):
    source          = forms.ImageField()

    class Meta:
        model       = Picture
        exclude     = ['date_created', 'title', 'description', 'picture_width', 'picture_height']
        
    class Media:
        js          = (settings.STATIC_URL + 'js/picture.upload.js',)
        
    def clean_source(self):
        if self.cleaned_data.get('source'):
            picture = self.cleaned_data['source']
            if 'error' in picture:
                raise forms.ValidationError(_('Upload a valid picture. \
                        The file you uploaded was either not an picture or a corrupted picture.'))
                
            content_type = picture.content_type
            if content_type:
                main, sub = content_type.split('/')
                if not (main == 'picture' and sub in ['jpeg', 'gif', 'png']):
                    raise forms.ValidationError(_('JPEG, PNG or GIF only.'))
        
            if picture.size > 1024 * 1024 * 2:
                raise forms.ValidationError(_('Image size too big, max allowed size is 2MB'))
            """
            x, y = Image.open(picture_data.temporary_file_path()).size
            if y < 128 or x < 128:  
                raise forms.ValidationError(_('Upload a valid picture. This one is too small in size.'))  
            """            
            return self.cleaned_data['source']

class PictureUpdateForm(forms.ModelForm):
    title               = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'class': 'title text' }))
    description         = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Picture
        fields      = ['title', 'description']
        exclude     = ['date_created', 'source', 'picture_width', 'picture_height']

