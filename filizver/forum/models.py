# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from filizver.topic.models import Topic
from filizver.topic.fields import AutoOneToOneField, JSONField

from filizver.text.models import Text

import defaults


MARKUP_CHOICES = [('bbcode', 'bbcode')]


class Category(models.Model):
    topic      = models.OneToOneField(Topic, related_name="forum_category")
    position    = models.IntegerField(_('Position'), blank=True, default=0)
    groups      = models.ManyToManyField(Group, blank=True, null=True, 
                        help_text=_('Only users from these groups can see this category'))

    class Meta:
        ordering = ['position']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.topic.title

    def forum_count(self):
        return self.forums.all().count()

    @property
    def threads(self):
        return Thread.objects.filter(forum__category__id=self.id).select_related()

    @property
    def replies(self):
        return Reply.objects.filter(thread__forum__category__id=self.id).select_related()

    def has_access(self, user):
        if user.is_superuser:
            return True
        if self.groups.exists():
            if user.is_authenticated():
                if not self.groups.filter(user__pk=user.id).exists():
                    return False
            else:
                return False
        return True


class Forum(models.Model):
    category        = models.ForeignKey(Category, related_name='forums', verbose_name=_('Category'))
    topic           = models.OneToOneField(Topic)
    position        = models.IntegerField(_('Position'), blank=True, default=0)
    description     = models.TextField(_('Description'), blank=True, default='')
    moderators      = models.ManyToManyField(User, blank=True, null=True, verbose_name=_('Moderators'))
    last_update     = models.DateTimeField(_('Last update'), auto_now=True, blank=True, null=True)
    reply_count     = models.IntegerField(_('Reply count'), blank=True, default=0)
    thread_count    = models.IntegerField(_('Thread count'), blank=True, default=0)
    last_reply      = models.ForeignKey('Reply', related_name='last_forum_reply', blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.topic.title
        
    def title(self):
        return self.topic.title

    @models.permalink
    def get_absolute_url(self):
        return ('forum:forum', [self.id])

    @property
    def replies(self):
        return Reply.objects.filter(thread__forum__id=self.id).select_related()


class Thread(models.Model):
    forum           = models.ForeignKey(Forum, related_name='threads')
    topic           = models.OneToOneField(Topic, related_name='forum_thread')
    sticky          = models.BooleanField(_('Sticky'), blank=True, default=False)
    closed          = models.BooleanField(_('Closed'), blank=True, default=False)
    subscribers     = models.ManyToManyField(User, related_name='forum_subscriptions', verbose_name=_('Subscribers'), blank=True)
    view_count      = models.IntegerField(_('Views count'), blank=True, default=0)
    reply_count     = models.IntegerField(_('Reply count'), blank=True, default=0)
    last_update     = models.DateTimeField(_('Last update'), null=True)
    last_reply      = models.ForeignKey('Reply', related_name='last_thread_reply', blank=True, null=True)

    class Meta:
        ordering = ['-topic__created_date']
        get_latest_by = 'topic__updated_date'
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')

    def __unicode__(self):
        return '%s - %s' % (self.topic, self.forum)

    def delete(self, *args, **kwargs):
        try:
            last_reply = self.replies.latest()
            last_reply.last_forum_reply.clear()
        except Reply.DoesNotExist:
            pass
        else:
            last_reply.last_forum_reply.clear()
        forum = self.forum
        super(Thread, self).delete(*args, **kwargs)
        try:
            forum.last_reply = Thread.objects.filter(forum__id=forum.id).latest().last_reply
        except Thread.DoesNotExist:
            forum.last_reply = None
        forum.thread_count = Thread.objects.filter(forum__id=forum.id).count()
        forum.reply_count = Reply.objects.filter(thread__forum__id=forum.id).count()
        forum.save()

    @property
    def head(self):
        try:
            return self.replies.select_related().order_by('created_date')[0]
        except IndexError:
            return None

    # @property
    # def reply_count(self):
    #     return self.reply_count

    @models.permalink
    def get_absolute_url(self):
        return ('forum:thread', [self.id])

    def update_read(self, user):
        tracking = user.replytracking
        #if last_read > last_read - don't check threads
        if tracking.last_read and (tracking.last_read > self.last_reply.created):
            return
        if isinstance(tracking.threads, dict):
            #clear threads if len > 5Kb and set last_read to current time
            if len(tracking.threads) > 5120:
                tracking.threads = None
                tracking.last_read = datetime.now()
                tracking.save()
            #update threads if exist new reply or does't exist in dict
            if self.last_reply_id > tracking.threads.get(str(self.id), 0):
                tracking.threads[str(self.id)] = self.last_reply_id
                tracking.save()
        else:
            #initialize thread tracking dict
            tracking.threads = {self.id: self.last_reply_id}
            tracking.save()
    

class Reply(Text):
    text        = models.OneToOneField(Text, parent_link=True)
    thread      = models.ForeignKey(Thread, related_name='replies', verbose_name=_('Thread'))

    class Meta:
        ordering = ['created_date']
        get_latest_by = 'created_date'
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')

    def delete(self, *args, **kwargs):
        self_id = self.id
        head_id = self.thread.replies.order_by('created_date')[0].id
        forum = self.thread.forum
        thread = self.thread
        profile = self.user.get_profile()
        self.last_thread_reply.clear()
        self.last_forum_reply.clear()
        super(Reply, self).delete(*args, **kwargs)
        #if reply was last in thread - remove thread
        if self_id == head_id:
            thread.delete()
        else:
            try:
                thread.last_reply = Reply.objects.filter(thread__id=thread.id).latest()
            except Reply.DoesNotExist:
                thread.last_reply = None
            thread.reply_count = Reply.objects.filter(thread__id=thread.id).count()
            thread.save()
        try:
            forum.last_reply = Reply.objects.filter(thread__forum__id=forum.id).latest()
        except Reply.DoesNotExist:
            forum.last_reply = None
        #TODO: for speedup - save/update only changed fields
        forum.reply_count = Reply.objects.filter(thread__forum__id=forum.id).count()
        forum.thread_count = Thread.objects.filter(forum__id=forum.id).count()
        forum.save()
        profile.reply_count = Reply.objects.filter(user__id=self.user_id).count()
        profile.save()

    @models.permalink
    def get_absolute_url(self):
        return ('forum:reply', [self.id])

    def summary(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail

    __unicode__ = summary


class ReplyTracking(models.Model):
    """
    Model for tracking read/unread replies.
    In thread stored ids of threads and last_replies as dict.
    """

    user = AutoOneToOneField(User)
    threads = JSONField(null=True, blank=True)
    last_read = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Reply tracking')
        verbose_name_plural = _('Reply tracking')

    def __unicode__(self):
        return self.user.username



from .signals import reply_saved, thread_saved

post_save.connect(reply_saved, sender=Reply, dispatch_uid='forums_reply_save')
post_save.connect(thread_saved, sender=Thread, dispatch_uid='forums_thread_save')
