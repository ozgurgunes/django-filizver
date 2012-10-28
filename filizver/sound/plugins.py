# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryType
from .forms import SoundForm

class SoundEntryPlugin(EntryType):
    name = 'sound'
    title = 'Sound'
    form_class = SoundForm
    link = reverse('filizver:sound_create')
