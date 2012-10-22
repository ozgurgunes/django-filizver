# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


# urlpatterns = patterns('',
# 
#     url(r'^$', 'view_name', name='url_name'),
# 
# )
from django.conf.urls.defaults import *

from filizver.forum import defaults
from filizver.forum import views as forum_views
from filizver.forum.feeds import LastReplies, LastThreads, LastRepliesOnForum, \
     LastRepliesOnCategory, LastRepliesOnThread


urlpatterns = patterns('',

    # Forum
    url('^$', forum_views.index, name='index'),
    url('^(?P<forum_id>\d+)/$', forum_views.show_forum, name='forum'),
    url('^moderate/(?P<forum_id>\d+)/$', forum_views.moderate, name='moderate'),
    url('^search/$', forum_views.search, name='search'),
    url('^misc/$', forum_views.misc, name='misc'),

    # Thread
    url('^thread/(?P<thread_id>\d+)/$', forum_views.show_thread, name='thread'),
    url('^(?P<forum_id>\d+)/thread/add/$', forum_views.add_thread, name='add_thread'),
    url('^thread/(?P<thread_id>\d+)/delete_replies/$', forum_views.delete_replies, name='delete_replies'),
    url('^thread/move/$', forum_views.move_thread, name='move_thread'),
    url('^thread/(?P<thread_id>\d+)/stick_unstick/(?P<action>[s|u])/$', forum_views.stick_unstick_thread, name='stick_unstick_thread'),
    url('^thread/(?P<thread_id>\d+)/open_close/(?P<action>[c|o])/$', forum_views.open_close_thread, name='open_close_thread'),

    # Post
    url('^reply/(?P<reply_id>\d+)/$', forum_views.show_reply, name='reply'),
    url('^reply/(?P<reply_id>\d+)/edit/$', forum_views.edit_reply, name='edit_reply'),
    url('^reply/(?P<reply_id>\d+)/delete/$', forum_views.delete_reply, name='delete_reply'),
    # Post preview
    url(r'^preview/$', forum_views.reply_preview, name='reply_preview'),

    # Subscription
    url('^subscription/thread/(?P<thread_id>\d+)/delete/$', forum_views.delete_subscription, name='forum_delete_subscription'),
    url('^subscription/thread/(?P<thread_id>\d+)/add/$', forum_views.add_subscription, name='forum_add_subscription'),

    # Feeds
    url(r'^feeds/replies/$', LastReplies(), name='forum_replies_feed'),
    url(r'^feeds/threads/$', LastThreads(), name='forum_threads_feed'),
    url(r'^feeds/thread/(?P<thread_id>\d+)/$', LastRepliesOnThread(), name='forum_thread_feed'),
    url(r'^feeds/forum/(?P<forum_id>\d+)/$', LastRepliesOnForum(), name='forum_forum_feed'),
    url(r'^feeds/category/(?P<category_id>\d+)/$', LastRepliesOnCategory(), name='forum_category_feed'),

)
