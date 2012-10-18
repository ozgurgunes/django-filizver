# -*- coding: utf-8 -*-
from filizver.plugins import EntryType
from .forms import PictureForm

class PictureEntry(EntryType):
    name = 'picture'
    title = 'Picture'
    form_class = PictureForm
