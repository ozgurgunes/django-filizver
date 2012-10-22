# -*- coding: utf-8 -*-
from filizver.topic.plugins import TopicInline
from .admin import ForumInline, CategoryInline, ThreadInline


class ForumInlinePlugin(TopicInline):
    name = 'forum-inline'
    title = 'Forum Inline'
    inline = ForumInline

class CategoryInlinePlugin(TopicInline):
    name = 'category-inline'
    title = 'Category Inline'
    inline = CategoryInline

class ThreadInlinePlugin(TopicInline):
    name = 'thread-inline'
    title = 'Thread Inline'
    inline = ThreadInline

