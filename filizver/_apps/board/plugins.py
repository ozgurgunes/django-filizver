# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from filizver.core.plugins import MenuPoint
from filizver.topic.plugins import TopicPoint
from forms import BoardForm
from admin import BoardInline

class BoardTopic(TopicPoint):
    name = 'board'
    title = 'Board'
    form_class = BoardForm
    admin_inline = BoardInline
    #link = reverse('board:board_create')
        
    def create(self, request):
        return super(BoardTopic, self).create(request)

class BoardMenu(MenuPoint):
    name = 'board-menu'
    title = 'Board Menu'

    def get_link(self):
        return reverse('board:board_list')

    def get_label(self):
        return _('Boards')
