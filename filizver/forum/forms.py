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
from filizver.forum.utils import set_language


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

    name = forms.CharField(label=_('Subject'), max_length=255,
                           widget=forms.TextInput(attrs={'size':'115'}))
    attachment = forms.FileField(label=_('Attachment'), required=False)
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
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['name'].required = False

        self.fields['body'].widget = forms.Textarea(attrs={'class':'markup', 'rows':'20', 'cols':'95'})

        if not defaults.ATTACHMENT_SUPPORT:
            self.fields['attachment'].widget = forms.HiddenInput()
            self.fields['attachment'].required = False

    def clean(self):
        '''
        checking is reply subject and body contains not only space characters
        '''
        errmsg = _('Can\'t be empty nor contain only whitespace characters')
        cleaned_data = self.cleaned_data
        body = cleaned_data.get('body')
        subject = cleaned_data.get('name')
        if subject:
            if not subject.strip():
                self._errors['name'] = self.error_class([errmsg])
                del cleaned_data['name']
        if body:
            if not body.strip():
                self._errors['body'] = self.error_class([errmsg])
                del cleaned_data['body']
        return cleaned_data

    def clean_attachment(self):
        if self.cleaned_data['attachment']:
            memfile = self.cleaned_data['attachment']
            if memfile.size > defaults.ATTACHMENT_SIZE_LIMIT:
                raise forms.ValidationError(_('Attachment is too big'))
            return self.cleaned_data['attachment']

    def save(self):
        if self.forum:
            thread = Thread(forum=self.forum,
                          user=self.user,
                          name=self.cleaned_data['name'])
            thread.save()
        else:
            thread = self.thread

        if self.cleaned_data['subscribe']:
            # User would like to subscripe to this thread
            thread.subscribers.add(self.user)

        reply = Reply(thread=thread, user=self.user, user_ip=self.ip,
                    markup=self.user.forum_profile.markup,
                    body=self.cleaned_data['body'])

        reply.save()
        if defaults.ATTACHMENT_SUPPORT:
            self.save_attachment(reply, self.cleaned_data['attachment'])
        return reply


    def save_attachment(self, reply, memfile):
        if memfile:
            obj = Attachment(size=memfile.size, content_type=memfile.content_type,
                             name=memfile.name, reply=reply)
            dir = os.path.join(settings.MEDIA_ROOT, defaults.ATTACHMENT_UPLOAD_TO)
            fname = '%d.0' % reply.id
            path = os.path.join(dir, fname)
            file(path, 'wb').write(memfile.read())
            obj.path = fname
            obj.save()


class EditReplyForm(forms.ModelForm):
    name = forms.CharField(required=False, label=_('Subject'),
                           widget=forms.TextInput(attrs={'size':'115'}))

    class Meta:
        model = Reply
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread', None)
        super(EditReplyForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.thread
        self.fields['body'].widget = forms.Textarea(attrs={'class':'markup'})

    def save(self, commit=True):
        reply = super(EditReplyForm, self).save(commit=False)
        reply.updated_date = datetime.now()
        thread_name = self.cleaned_data['name']
        if thread_name:
            reply.thread.name = thread_name
        if commit:
            reply.thread.save()
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


