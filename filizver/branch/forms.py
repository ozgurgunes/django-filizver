# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User

from filizver.topic.models import Topic
from filizver.branch.models import Branch
from filizver.branch.lookups import BranchLookup

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
        attrs[u'rows'] = 2
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
                

class BranchForm(forms.ModelForm):
    topic           = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput)
    # source          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
    #                             widget=forms.TextInput(attrs={ 'class': 'branch text' }))
    source          = forms.ModelChoiceField(queryset=Topic.objects.all(), 
                            widget=AutoCompleteSelectWidget(BranchLookup, 
                                attrs={'placeholder': _('Branch out')}))

    class Meta:
        model       = Branch
        fields     = ['source']

