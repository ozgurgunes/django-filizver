# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.video import VideoForm


class VideoEntry(EntryPoint):
    name = 'video'
    title = 'Video'
    form_class = VideoForm
    link = reverse('filizver:video_create')
