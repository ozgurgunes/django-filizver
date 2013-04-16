from datetime import datetime

from django.db.models.signals import post_save

from filizver.forum.subscription import notify_thread_subscribers
from filizver.forum.models import Thread, Reply


def reply_saved(instance, **kwargs):
    created = kwargs.get('created')
    reply = instance
    thread = reply.thread

    if created:
        thread.last_reply = reply
        thread.reply_count = thread.replies.count()
        thread.last_update = datetime.now()
        profile = reply.text.user.get_profile()
        #profile.reply_count = reply.text.user.replies.count()
        profile.save(force_update=True)
        notify_thread_subscribers(reply)
    thread.save(force_update=True)


def thread_saved(instance, **kwargs):
    thread = instance
    forum = thread.forum
    forum.thread_count = forum.threads.count()
    forum.last_update = thread.last_update
    forum.reply_count = forum.replies.count()
    forum.last_reply_id = thread.last_reply_id
    forum.save(force_update=True)
