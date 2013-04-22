# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.document import SoundForm


class SoundEntry(EntryPoint):
    name = 'sound'
    title = 'Sound'
    form_class = SoundForm
    link = reverse('filizver:sound_create')
