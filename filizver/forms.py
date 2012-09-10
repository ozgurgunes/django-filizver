# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User

from filizver.models import Topic, Entry, Branch, Image, Text
from filizver.lookups import BranchLookup

from selectable.forms.widgets import AutoCompleteSelectWidget

class TopicForm(forms.ModelForm):
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))
    class Meta:
        model       = Topic
        exclude     = ['user', 'slug', 'branches', 'tags', 'date_created', 'is_public']

class EntryForm(forms.ModelForm):
    branch          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
                            widget=AutoCompleteSelectWidget(BranchLookup, 
                                attrs={'placeholder': _('Branch out')}))

    text            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea markup', 'rows': 8, 'required': 'required'}))

    source          = forms.ImageField()

    class Meta:
        model       = Entry
        exclude     = ['user','topic', 'object_id', 'content_type', 'date_created']

    class Media:
        js          = (settings.STATIC_URL + 'js/image.upload.js',)
        

class BranchForm(forms.ModelForm):
    topic           = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput)
    # source          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
    #                             widget=forms.TextInput(attrs={ 'class': 'branch text' }))
    source          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
                            widget=AutoCompleteSelectWidget(BranchLookup, 
                                attrs={'placeholder': _('Branch out')}))

    class Meta:
        model       = Branch
        exclude     = ['date_created']

class ImageForm(forms.ModelForm):
    source          = forms.ImageField()

    class Meta:
        model       = Image
        exclude     = ['date_created', 'title', 'description', 'image_width', 'image_height']
        
    class Media:
        js          = (settings.STATIC_URL + 'js/image.upload.js',)
        
    def clean_image(self):
        from StringIO import StringIO  
        from PIL import Image

        if self.cleaned_data.get('source'):
            image = self.cleaned_data['source']
            if 'error' in image:
                raise forms.ValidationError(_('Upload a valid image. \
                        The file you uploaded was either not an image or a corrupted image.'))
                
            content_type = image.content_type
            if content_type:
                main, sub = content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                    raise forms.ValidationError(_('JPEG, PNG or GIF only.'))
        
            if image.size > 1024 * 1024 * 2:
                raise forms.ValidationError(_('Image size too big, max allowed size is 2MB'))
            """
            x, y = Image.open(image_data.temporary_file_path()).size
            if y < 128 or x < 128:  
                raise forms.ValidationError(_('Upload a valid image. This one is too small in size.'))  
            """            
            return self.cleaned_data['source']

class ImageUpdateForm(forms.ModelForm):
    title               = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'class': 'title text' }))
    description         = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Image
        fields      = ['title', 'description']
        exclude     = ['date_created', 'image', 'image_width', 'image_height']

class TextForm(forms.ModelForm):
    source            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea markup', 'rows': 8, 'required': 'required'}))
#    footnote        = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Text
        exclude     = ['date_created', 'footnote']
        
class TextUpdateForm(forms.ModelForm):
    source          = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 8}))

    class Meta:
        model       = Text
        exclude     = ['date_created', 'footnote']
