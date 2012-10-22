from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

from filizver.forum import defaults
from filizver.core.utils import absolute_url

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail
    def send_mail(subject, text, from_email, rec_list, html=None):
        """
        Shortcut for sending email.
        """
    
        msg = EmailMultiAlternatives(subject, text, from_email, rec_list)
        if html:
            msg.attach_alternative(html, "text/html")
        if defaults.EMAIL_DEBUG:
            print '---begin---'
            print 'To:', rec_list
            print 'Subject:', subject
            print 'Body:', text
            print '---end---'
        else:
            msg.send(fail_silently=True)


# TODO: move to txt template
TOPIC_SUBSCRIPTION_TEXT_TEMPLATE = (u"""New reply from %(username)s to thread that you have subscribed on.
---
%(message)s
---
See thread: %(reply_url)s
Unsubscribe %(unsubscribe_url)s""")


def notify_thread_subscribers(reply):
    thread = reply.thread
    reply_body_text = strip_tags(reply.body_html)
    if reply != thread.head:
        for user in thread.subscribers.all():
            if user != reply.user:
                subject = u'RE: %s' % thread.name
                to_email = user.email
                text_content = TOPIC_SUBSCRIPTION_TEXT_TEMPLATE % {
                        'username': reply.user.username,
                        'message': reply_body_text,
                        'reply_url': absolute_url(reply.get_absolute_url()),
                        'unsubscribe_url': absolute_url(reverse('forums:forum_delete_subscription', args=[reply.thread.id])),
                    }
                #html_content = html_version(reply)
                send_mail(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
