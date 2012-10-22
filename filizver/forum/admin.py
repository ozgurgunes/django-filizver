# coding: utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from filizver.core.admin import ReverseModelAdmin


from .models import Category, Forum, Thread, Reply, ReplyTracking

from filizver.topic.models import Topic


class BaseModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        # disabled, because delete_selected ignoring delete model method
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ForumInline(admin.StackedInline):
    model = Forum
    raw_id_fields = ('moderators', 'last_reply',)
    

class CategoryInline(admin.StackedInline):
    model = Category


class ThreadInline(admin.StackedInline):
    model = Thread
    raw_id_fields = ('subscribers',)


class CategoryAdmin(BaseModelAdmin):
    list_display = ['topic', 'position', 'forum_count']

class ForumAdmin(BaseModelAdmin):
    list_display = ['topic', 'category', 'position', 'thread_count']
    raw_id_fields = ['moderators', 'last_reply']

class ThreadAdmin(BaseModelAdmin):
    def subscribers2(self, obj):
        return ", ".join([user.username for user in obj.subscribers.all()])
    subscribers2.short_description = _("subscribers")

    list_display = ['topic', 'forum', 'head', 'reply_count', 'subscribers2']
    search_fields = ['topic']
    raw_id_fields = ['subscribers', 'last_reply']

class ReplyAdmin(BaseModelAdmin):
    list_display = ['topic', 'user', 'created_date', 'updated_date', 'summary']
    search_fields = ['body']
    raw_id_fields = ['topic', 'user']

class ReplyTrackingAdmin(BaseModelAdmin):
    list_display = ['user', 'last_read', 'threads']
    raw_id_fields = ['user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(ReplyTracking, ReplyTrackingAdmin)
