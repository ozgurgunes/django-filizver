# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.document import DocumentForm


class DocumentEntry(EntryPoint):
    name = 'document'
    title = 'Document'
    form_class = DocumentForm
    link = reverse('filizver:document_create')
