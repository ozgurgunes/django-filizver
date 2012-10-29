# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryPoint
from .forms import VideoForm

class VideoEntryPlugin(EntryPoint):
    name = 'video'
    title = 'Video'
    form_class = VideoForm
    link = reverse('filizver:video_create')
