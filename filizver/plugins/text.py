# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.text import TextForm


class TextEntry(EntryPoint):

    name = 'text'
    title = 'Text'
    form_class = TextForm
    link = reverse('filizver:text_create')
