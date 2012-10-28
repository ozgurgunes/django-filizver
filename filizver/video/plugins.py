# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryType
from .forms import VideoForm

class VideoEntryPlugin(EntryType):
    name = 'video'
    title = 'Video'
    form_class = VideoForm
    link = reverse('filizver:video_create')
