# coding: utf-8

import os.path
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.utils.translation import ugettext_lazy as _

from filizver.forum.models import Thread, Reply
from filizver.forum import defaults
from filizver.text.utils import text_to_html
from filizver.core.utils import set_language
from filizver.topic.models import Topic

SORT_USER_BY_CHOICES = (
    ('username', _(u'Username')),
    ('registered', _(u'Registered')),
    ('num_replies', _(u'No. of replies')),
)

SORT_POST_BY_CHOICES = (
    ('0', _(u'Reply time')),
    ('1', _(u'Author')),
    ('2', _(u'Subject')),
    ('3', _(u'Forum')),
)

SORT_DIR_CHOICES = (
    ('ASC', _(u'Ascending')),
    ('DESC', _(u'Descending')),
)

SHOW_AS_CHOICES = (
    ('threads', _(u'Threads')),
    ('replies', _(u'Replies')),
)

SEARCH_IN_CHOICES = (
    ('all', _(u'Message text and thread subject')),
    ('message', _(u'Message text only')),
    ('thread', _(u'Thread subject only')),
)


class AddReplyForm(forms.ModelForm):
    FORM_NAME = "AddReplyForm" # used in view and template submit button

    title = forms.CharField(label=_('Subject'), max_length=255,
                           widget=forms.TextInput(attrs={'size':'115'}))
    subscribe = forms.BooleanField(label=_('Subscribe'), help_text=_("Subscribe this thread."), required=False)

    class Meta:
        model = Reply
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.thread = kwargs.pop('thread', None)
        self.forum = kwargs.pop('forum', None)
        self.ip = kwargs.pop('ip', None)
        super(AddReplyForm, self).__init__(*args, **kwargs)

        if self.thread:
            self.fields['title'].widget = forms.HiddenInput()
            self.fields['title'].required = False

        self.fields['body'].widget = forms.Textarea(attrs={'class':'markup'})

    def clean(self):
        '''
        checking is reply subject and body contains not only space characters
        '''
        errmsg = _('Can\'t be empty nor contain only whitespace characters')
        cleaned_data = self.cleaned_data
        body = cleaned_data.get('body')
        subject = cleaned_data.get('title')
        if subject:
            if not subject.strip():
                self._errors['title'] = self.error_class([errmsg])
                del cleaned_data['title']
        if body:
            if not body.strip():
                self._errors['body'] = self.error_class([errmsg])
                del cleaned_data['body']
        return cleaned_data

    def save(self):
        if self.forum:
            topic = Topic(title=self.cleaned_data['title'], user=self.user)
            topic.save()
            thread = Thread(forum=self.forum, topic=topic)
            thread.save()
        else:
            thread = self.thread

        if self.cleaned_data['subscribe']:
            # User would like to subscripe to this thread
            thread.subscribers.add(self.user)

        reply = Reply(thread=thread, topic=thread.topic, user=self.user,
                    body=self.cleaned_data['body'])

        reply.save()
        return reply


    def save_attachment(self, reply, memfile):
        if memfile:
            obj = Attachment(size=memfile.size, content_type=memfile.content_type,
                             name=memfile.topic.title, reply=reply)
            dir = os.path.join(settings.MEDIA_ROOT, defaults.ATTACHMENT_UPLOAD_TO)
            fname = '%d.0' % reply.id
            path = os.path.join(dir, fname)
            file(path, 'wb').write(memfile.read())
            obj.path = fname
            obj.save()


class EditReplyForm(forms.ModelForm):
    title = forms.CharField(required=False, label=_('Subject'),
                           widget=forms.TextInput(attrs={'size':'115'}))

    class Meta:
        model = Reply
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread', None)
        super(EditReplyForm, self).__init__(*args, **kwargs)
        self.fields['title'].initial = self.thread.topic.title
        self.fields['body'].widget = forms.Textarea(attrs={'class':'markup'})

    def save(self, commit=True):
        reply = super(EditReplyForm, self).save(commit=False)
        reply.updated_date = datetime.now()
        thread_name = self.cleaned_data['title']
        if thread_name:
            reply.thread.topic.title = thread_name
        if commit:
            reply.thread.topic.save()
            reply.save()
        return reply


class ReplySearchForm(forms.Form):
    keywords = forms.CharField(required=False, label=_('Keyword search'),
                               widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100'}))
    author = forms.CharField(required=False, label=_('Author search'),
                             widget=forms.TextInput(attrs={'size':'25', 'maxlength':'25'}))
    forum = forms.CharField(required=False, label=_('Forum'))
    search_in = forms.ChoiceField(choices=SEARCH_IN_CHOICES, label=_('Search in'))
    sort_by = forms.ChoiceField(choices=SORT_POST_BY_CHOICES, label=_('Sort by'))
    sort_dir = forms.ChoiceField(choices=SORT_DIR_CHOICES, initial='DESC', label=_('Sort order'))
    show_as = forms.ChoiceField(choices=SHOW_AS_CHOICES, label=_('Show results as'))


class MailToForm(forms.Form):
    subject = forms.CharField(label=_('Subject'),
                              widget=forms.TextInput(attrs={'size':'75', 'maxlength':'70', 'class':'longinput'}))
    body = forms.CharField(required=False, label=_('Message'),
                               widget=forms.Textarea(attrs={'rows':'10', 'cols':'75'}))


