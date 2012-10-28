# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryType
from forms import TextForm

class TextEntryPlugin(EntryType):
    name = 'text'
    title = 'Text'
    form_class = TextForm
    link = reverse('filizver:text_create')
        
    def create(self, request):
        return super(TextEntryPlugin, self).create(request)
