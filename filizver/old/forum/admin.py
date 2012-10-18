# -*- coding: utf-8

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf import settings

from filizver.forum.models import Category, Forum, Topic, Post, Profile


class ForumInlineAdmin(admin.TabularInline):
    model = Forum
    fields = ['topic', 'hidden', 'position']
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['topic', 'position', 'hidden', 'forum_count']
    list_per_page = 20
    ordering = ['position']
    search_fields = ['topic']
    list_editable = ['position']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['topic', 'category', 'hidden', 'position', 'topic_count', ]
    list_per_page = 20
    raw_id_fields = ['moderators']
    ordering = ['-category']
    search_fields = ['topic', 'category__topic']
    list_editable = ['position', 'hidden']
    fieldsets = (
        (None, {
                'fields': ('category', 'topic', 'hidden', 'position', )
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields': ('description', 'headline', 'post_count', 'moderators')
                }
            ),
        )


class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'forum', 'date_created', 'head',]
    list_per_page = 20
    #raw_id_fields = ['user', 'subscribers']
    ordering = ['-date_created']
    date_hierarchy = 'date_created'
    search_fields = ['topic']
    fieldsets = (
        (None, {
                'fields': ('title', 'user',)
                }
         ),
        # (_('Additional options'), {
        #         'classes': ('collapse',),
        #         'fields': (('views', 'post_count'), ('sticky', 'closed'), 'subscribers')
        #         }
        #  ),
        )

class TopicReadTrackerAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'time_stamp']
    search_fields = ['user__usertopic']

class ForumReadTrackerAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'time_stamp']
    search_fields = ['user__usertopic']

class PostAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'date_created', 'summary']
    list_per_page = 20
    raw_id_fields = ['user', 'topic']
    ordering = ['-date_created']
    date_hierarchy = 'date_created'
    search_fields = ['source']
    fieldsets = (
        (None, {
                'fields': ('topic', 'user')
                }
         ),
        # (_('Additional options'), {
        #         'classes': ('collapse',),
        #         'fields' : (('date_created', 'updated'), 'user_ip')
        #         }
        #  ),
        # (_('Message'), {
        #         'fields': ('body', 'body_html', 'body_text')
        #         }
        #  ),
        )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_zone', 'language']
    list_per_page = 20
    ordering = ['-user']
    search_fields = ['user__usertopic', 'user__first_topic', 'user__last_topic']
    fieldsets = (
        (None, {
                'fields': ('time_zone', 'language')
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields' : ('avatar', 'signature', 'show_signatures')
                }
         ),
        )




admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)

if settings.AUTH_PROFILE_MODULE == 'forum.Profile':
    admin.site.register(Profile, ProfileAdmin)

# This can be used to debug read/unread trackers

#admin.site.register(TopicReadTracker, TopicReadTrackerAdmin)
#admin.site.register(ForumReadTracker, ForumReadTrackerAdmin)