# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryPoint
from .forms import SoundForm

class SoundEntryPlugin(EntryPoint):
    name = 'sound'
    title = 'Sound'
    form_class = SoundForm
    link = reverse('filizver:sound_create')
