# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User

from filizver.models import Topic, Entry, Branch, Image, Text
from filizver.lookups import BranchLookup

from selectable.forms.widgets import SelectableMultiWidget, SelectableMediaMixin

class AutoCompleteWidget(forms.Textarea, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.qs = kwargs.pop('query_params', {})
        self.limit = kwargs.pop('limit', None)
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def update_query_parameters(self, qs_dict):
        self.qs.update(qs_dict)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoCompleteWidget, self).build_attrs(extra_attrs, **kwargs)
        url = self.lookup_class.url()
        if self.limit and 'limit' not in self.qs:
            self.qs['limit'] = self.limit
        if self.qs:
            url = '%s?%s' % (url, urlencode(self.qs))
        attrs[u'data-selectable-url'] = url
        attrs[u'data-selectable-type'] = 'text'
        attrs[u'data-selectable-allow-new'] = str(self.allow_new).lower()
        return attrs


class SelectableMultiWidget(forms.MultiWidget):

    def update_query_parameters(self, qs_dict):
        self.widgets[0].update_query_parameters(qs_dict)


class AutoCompleteSelectWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        query_params = kwargs.pop('query_params', {})
        widgets = [
            AutoCompleteWidget(
                lookup_class, allow_new=self.allow_new,
                limit=self.limit, query_params=query_params
            ),
            forms.HiddenInput(attrs={u'data-selectable-type': 'hidden'})
        ]
        super(AutoCompleteSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            model = getattr(self.lookup_class, 'model', None)
            if model and isinstance(value, model):
                item = value
                value = lookup.get_item_id(item)
            else:
                item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        value = super(AutoCompleteSelectWidget, self).value_from_datadict(data, files, name)
        if not self.allow_new:
            return value[1]
        return value


class TopicForm(forms.ModelForm):
    title           = forms.CharField(max_length=128, widget=forms.TextInput(
                                attrs={'class': 'title input', 'placeholder': _('Type your topic title')}
                                ))
    class Meta:
        model       = Topic
        exclude     = ['user', 'slug', 'branches', 'tags', 'date_created', 'is_public']

class EntryForm(forms.ModelForm):
    body          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
                            widget=AutoCompleteSelectWidget(BranchLookup, 
                                attrs={'placeholder': _('Branch out')}))
    
    # text            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea markup', 'rows': 8, 'required': 'required'}))

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
        
    def clean_source(self):
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
        exclude     = ['date_created', 'source', 'image_width', 'image_height']

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
