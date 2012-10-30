# -*- coding: utf-8 -*-
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
