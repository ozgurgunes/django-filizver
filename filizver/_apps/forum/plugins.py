# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from filizver.core.plugins import MenuPoint
from filizver.topic.plugins import TopicPoint
from .admin import ForumInline, CategoryInline, ThreadInline


class CategoryTopic(TopicPoint):
    name = 'category-inline'
    title = 'Category Topic'
    admin_inline = CategoryInline

class ThreadTopic(TopicPoint):
    name = 'thread-topic'
    title = 'Thread Topic'
    admin_inline = ThreadInline

class ForumTopic(TopicPoint):
    name = 'forum-topic'
    title= 'Forum Topic'
    admin_inline = ForumInline

class ForumMenu(MenuPoint):
    name = 'forum-menu'
    title = 'Forum Menu'
    
    def get_link(self):
        return reverse('forum:index')

    def get_label(self):
        return _('Forum')
