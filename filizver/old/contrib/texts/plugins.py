# -*- coding: utf-8 -*-
from filizver.plugins import EntryType
from .forms import TextForm

class TextEntry(EntryType):
    name = 'text'
    title = 'Text'
    form_class = TextForm