# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryPoint
from forms import DocumentForm

class DocumentEntryPlugin(EntryPoint):
    name = 'document'
    title = 'Document'
    form_class = DocumentForm
    link = reverse('filizver:document_create')
