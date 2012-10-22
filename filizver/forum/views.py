# coding: utf-8

import math
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q, F
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from haystack.query import SearchQuerySet, SQ

from filizver.forum import defaults
from filizver.forum.forms import AddReplyForm, EditReplyForm, ReplySearchForm, MailToForm
from filizver.forum.models import Category, Forum, Thread, Reply, ReplyTracking
from filizver.forum.templatetags import forum_tags
from filizver.forum.templatetags.forum_tags import forum_moderated_by
from filizver.topic.utils import build_form, paginate, set_language
from filizver.text.utils import smileys, text_to_html




def index(request, full=True):
    users_cached = cache.get('forums_users_online', {})
    users_online = users_cached and User.objects.filter(id__in=users_cached.keys()) or []
    guests_cached = cache.get('forums_guests_online', {})
    guest_count = len(guests_cached)
    users_count = len(users_online)

    _forums = Forum.objects.all()
    user = request.user
    if not user.is_superuser:
        user_groups = user.groups.all() or [] # need 'or []' for anonymous user otherwise: 'EmptyManager' object is not iterable
        _forums = _forums.filter(Q(category__groups__in=user_groups) | Q(category__groups__isnull=True))

    _forums = _forums.select_related('last_reply__thread', 'last_reply__user', 'category')

    cats = {}
    forums = {}
    for forum in _forums:
        cat = cats.setdefault(forum.category.id,
            {'id': forum.category.id, 'cat': forum.category, 'forums': []})
        cat['forums'].append(forum)
        forums[forum.id] = forum

    cmpdef = lambda a, b: cmp(a['cat'].position, b['cat'].position)
    cats = sorted(cats.values(), cmpdef)

    to_return = {'cats': cats,
                'replies': Reply.objects.count(),
                'threads': Thread.objects.count(),
                'users': User.objects.count(),
                'users_online': users_online,
                'online_count': users_count,
                'guest_count': guest_count,
                'last_user': User.objects.latest('date_joined'),
                }
    if full:
        return render(request, 'forums/index.html', to_return)
    else:
        return render(request, 'forums/lofi/index.html', to_return)


@transaction.commit_on_success
def moderate(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    threads = forum.threads.order_by('-sticky', '-updated_date').select_related()
    if request.user.is_superuser or request.user in forum.moderators.all():
        thread_ids = request.POST.getlist('thread_id')
        if 'move_threads' in request.POST:
            return render(request, 'forums/move_thread.html', {
                'categories': Category.objects.all(),
                'thread_ids': thread_ids,
                'exclude_forum': forum,
            })
        elif 'delete_threads' in request.POST:
            for thread_id in thread_ids:
                thread = get_object_or_404(Thread, pk=thread_id)
                thread.delete()
            messages.success(request, _("Threads deleted"))
            return HttpResponseRedirect(reverse('forums:index'))
        elif 'open_threads' in request.POST:
            for thread_id in thread_ids:
                open_close_thread(request, thread_id, 'o')
            messages.success(request, _("Threads opened"))
            return HttpResponseRedirect(reverse('forums:index'))
        elif 'close_threads' in request.POST:
            for thread_id in thread_ids:
                open_close_thread(request, thread_id, 'c')
            messages.success(request, _("Threads closed"))
            return HttpResponseRedirect(reverse('forums:index'))

        return render(request, 'forums/moderate.html', {'forum': forum,
                'threads': threads,
                #'sticky_threads': forum.threads.filter(sticky=True),
                'replies': forum.replies.count(),
                })
    else:
        raise Http404


def search(request):
    # TODO: used forms in every search type

    def _render_search_form(form=None):
        return render(request, 'forums/search_form.html', {'categories': Category.objects.all(),
                'form': form,
                })

    if not 'action' in request.GET:
        return _render_search_form(form=ReplySearchForm())

    if request.GET.get("show_as") == "replies":
        show_as_replies = True
        template_name = 'forums/search_replies.html'
    else:
        show_as_replies = False
        template_name = 'forums/search_threads.html'

    context = {}

    # Create 'user viewable' pre-filtered threads/replies querysets
    viewable_category = Category.objects.all()
    threads = Thread.objects.all().order_by("-last_reply__created_date")
    replies = Reply.objects.all().order_by('-created_date')
    user = request.user
    if not user.is_superuser:
        user_groups = user.groups.all() or [] # need 'or []' for anonymous user otherwise: 'EmptyManager' object is not iterable 
        viewable_category = viewable_category.filter(Q(groups__in=user_groups) | Q(groups__isnull=True))

        threads = Thread.objects.filter(forum__category__in=viewable_category)
        replies = Reply.objects.filter(thread__forum__category__in=viewable_category)

    base_url = None
    _generic_context = True

    action = request.GET['action']
    if action == 'show_24h':
        date = datetime.now() - timedelta(days=1)
        if show_as_replies:
            context["replies"] = replies.filter(Q(created_date__gte=date) | Q(updated_date__gte=date))
        else:
            context["threads"] = threads.filter(Q(last_reply__created_date__gte=date) | Q(last_reply__updated_date__gte=date))
        _generic_context = False
    elif action == 'show_new':
        if not user.is_authenticated():
            raise Http404("Search 'show_new' not available for anonymous user.")
        try:
            last_read = ReplyTracking.objects.get(user=user).last_read
        except ReplyTracking.DoesNotExist:
            last_read = None

        if last_read:
            if show_as_replies:
                context["replies"] = replies.filter(Q(created_date__gte=last_read) | Q(updated_date__gte=last_read))
            else:
                context["threads"] = threads.filter(Q(last_reply__created_date__gte=last_read) | Q(last_reply__updated_date__gte=last_read))
            _generic_context = False
        else:
            #searching more than defaults.SEARCH_PAGE_SIZE in this way - not good idea :]
            threads = [thread for thread in threads[:defaults.SEARCH_PAGE_SIZE] if forum_tags.has_unreads(thread, user)]
    elif action == 'show_unanswered':
        threads = threads.filter(reply_count=1)
    elif action == 'show_subscriptions':
        threads = threads.filter(subscribers__id=user.id)
    elif action == 'show_user':
        # Show all replies from user or threads started by user
        if not user.is_authenticated():
            raise Http404("Search 'show_user' not available for anonymous user.")

        if user.is_staff:
            user_id = request.GET.get("user_id", user.id)
            user_id = int(user_id)
            if user_id != user.id:
                search_user = User.objects.get(id=user_id)
                messages.info(request, "Filter by user '%s'." % search_user.username)
        else:
            user_id = user.id

        if show_as_replies:
            replies = replies.filter(user__id=user_id)
        else:
            # show as thread
            threads = threads.filter(replies__user__id=user_id).order_by("-last_reply__created_date").distinct()

        base_url = "?action=show_user&user_id=%s&show_as=" % user_id
    elif action == 'search':
        form = ReplySearchForm(request.GET)
        if not form.is_valid():
            return _render_search_form(form)

        keywords = form.cleaned_data['keywords']
        author = form.cleaned_data['author']
        forum = form.cleaned_data['forum']
        search_in = form.cleaned_data['search_in']
        sort_by = form.cleaned_data['sort_by']
        sort_dir = form.cleaned_data['sort_dir']

        query = SearchQuerySet().models(Reply)

        if author:
            query = query.filter(author__username=author)

        if forum != u'0':
            query = query.filter(forum__id=forum)

        if keywords:
            if search_in == 'all':
                query = query.filter(SQ(thread=keywords) | SQ(text=keywords))
            elif search_in == 'message':
                query = query.filter(text=keywords)
            elif search_in == 'thread':
                query = query.filter(thread=keywords)

        order = {'0': 'created_date',
                 '1': 'author',
                 '2': 'thread',
                 '3': 'forum'}.get(sort_by, 'created_date')
        if sort_dir == 'DESC':
            order = '-' + order

        replies = query.order_by(order)

        if not show_as_replies:
            # TODO: We have here a problem to get a list of threads without double entries.
            # Maybe we must add a search index over threads?

            # Info: If whoosh backend used, setup HAYSTACK_ITERATOR_LOAD_PER_QUERY
            #    to a higher number to speed up
            reply_pks = replies.values_list("pk", flat=True)
            context["threads"] = threads.filter(replies__in=reply_pks).distinct()
        else:
            # FIXME: How to use the pre-filtered query from above?
            replies = replies.filter(thread__forum__category__in=viewable_category)
            context["replies"] = replies

        get_query_dict = request.GET.copy()
        get_query_dict.pop("show_as")
        base_url = "?%s&show_as=" % get_query_dict.urlencode()
        _generic_context = False

    if _generic_context:
        if show_as_replies:
            context["replies"] = replies.filter(thread__in=threads).order_by('-created_date')
        else:
            context["threads"] = threads

    if base_url is None:
        base_url = "?action=%s&show_as=" % action

    if show_as_replies:
        context["as_thread_url"] = base_url + "threads"
        reply_count = context["replies"].count()
        messages.success(request, _("Found %i replies.") % reply_count)
    else:
        context["as_reply_url"] = base_url + "replies"
        thread_count = context["threads"].count()
        messages.success(request, _("Found %i threads.") % thread_count)

    return render(request, template_name, context)




@login_required
def misc(request):
    if 'action' in request.GET:
        action = request.GET['action']
        if action == 'markread':
            user = request.user
            ReplyTracking.objects.filter(user__id=user.id).update(last_read=datetime.now(), threads=None)
            messages.info(request, _("All threads marked as read."))
            return HttpResponseRedirect(reverse('forums:index'))

        elif action == 'report':
            if request.GET.get('reply_id', ''):
                reply_id = request.GET['reply_id']
                reply = get_object_or_404(Reply, id=reply_id)
                form = build_form(ReportForm, request, reported_by=request.user, reply=reply_id)
                if request.method == 'POST' and form.is_valid():
                    form.save()
                    messages.info(request, _("Reply reported."))
                    return HttpResponseRedirect(reply.get_absolute_url())
                return render(request, 'forums/report.html', {'form':form})

    elif 'submit' in request.POST and 'mail_to' in request.GET:
        form = MailToForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=request.GET['mail_to'])
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body'] + u'\n %s %s [%s]' % (Site.objects.get_current().domain,
                                                                  request.user.username,
                                                                  request.user.email)
            try:
                user.email_user(subject, body, request.user.email)
                messages.success(request, _("Email send."))
            except Exception:
                messages.error(request, _("Email could not be sent."))
            return HttpResponseRedirect(reverse('forums:index'))

    elif 'mail_to' in request.GET:
        mailto = get_object_or_404(User, username=request.GET['mail_to'])
        form = MailToForm()
        return render(request, 'forums/mail_to.html', {'form':form,
                'mailto': mailto}
                )


def show_forum(request, forum_id, full=True):
    forum = get_object_or_404(Forum, pk=forum_id)
    if not forum.category.has_access(request.user):
        return HttpResponseForbidden()
    threads = forum.threads.order_by('-sticky', '-updated_date').select_related()
    moderator = request.user.is_superuser or\
        request.user in forum.moderators.all()
    to_return = {'categories': Category.objects.all(),
                'forum': forum,
                'replies': forum.reply_count,
                'threads': threads,
                'moderator': moderator,
                }
    if full:
        return render(request, 'forums/forum.html', to_return)
    else:
        return render(request, 'forums/lofi/forum.html', to_return)


@transaction.commit_on_success
def show_thread(request, thread_id, full=True):
    """
    * Display a thread
    * save a reply
    * save a poll vote
    
    TODO: Add reply in lofi mode
    """
    reply_request = request.method == "POST"
    user_is_authenticated = request.user.is_authenticated()
    if reply_request and not user_is_authenticated:
        # Info: only user that are logged in should get forms in the page.
        return HttpResponseForbidden()

    thread = get_object_or_404(Thread.objects.select_related(), pk=thread_id)
    if not thread.forum.category.has_access(request.user):
        return HttpResponseForbidden()
    Thread.objects.filter(pk=thread.id).update(views=F('views') + 1)

    last_reply = thread.last_reply

    if request.user.is_authenticated():
        thread.update_read(request.user)
    replies = thread.replies.all().select_related()

    moderator = request.user.is_superuser or request.user in thread.forum.moderators.all()
    if user_is_authenticated and request.user in thread.subscribers.all():
        subscribed = True
    else:
        subscribed = False

    # reply form
    reply_form = None
    form_url = None
    back_url = None
    if user_is_authenticated and not thread.closed:
        form_url = request.path + "#reply" # if form validation failed: browser should scroll down to reply form ;)
        back_url = request.path
        ip = request.META.get('REMOTE_ADDR', None)
        reply_form_kwargs = {"thread":thread, "user":request.user, "ip":ip}
        if reply_request and AddReplyForm.FORM_NAME in request.POST:
            reply_form = AddReplyForm(request.POST, request.FILES, **reply_form_kwargs)
            if reply_form.is_valid():
                reply = reply_form.save()
                messages.success(request, _("Your reply saved."))
                return HttpResponseRedirect(reply.get_absolute_url())
        else:
            reply_form = AddReplyForm(
                initial={
                    'markup': request.user.forum_profile.markup,
                    'subscribe': request.user.forum_profile.auto_subscribe,
                },
                **reply_form_kwargs
            )

    # handle poll, if exists
    poll_form = None
    polls = thread.poll_set.all()
    if not polls:
        poll = None
    else:
        poll = polls[0]
        if user_is_authenticated: # Only logged in users can vote
            poll.auto_deactivate()
            has_voted = request.user in poll.users.all()
            if not reply_request or not VotePollForm.FORM_NAME in request.POST:
                # It's not a POST request or: The reply form was send and not a poll vote
                if poll.active and not has_voted:
                    poll_form = VotePollForm(poll)
            else:
                if not poll.active:
                    messages.error(request, _("This poll is not active!"))
                    return HttpResponseRedirect(thread.get_absolute_url())
                elif has_voted:
                    messages.error(request, _("You have already vote to this poll in the past!"))
                    return HttpResponseRedirect(thread.get_absolute_url())

                poll_form = VotePollForm(poll, request.POST)
                if poll_form.is_valid():
                    ids = poll_form.cleaned_data["choice"]
                    queryset = poll.choices.filter(id__in=ids)
                    queryset.update(votes=F('votes') + 1)
                    poll.users.add(request.user) # save that this user has vote
                    messages.success(request, _("Your votes are saved."))
                    return HttpResponseRedirect(thread.get_absolute_url())

    highlight_word = request.GET.get('hl', '')
    if full:
        return render(request, 'forums/thread.html', {'categories': Category.objects.all(),
                'thread': thread,
                'last_reply': last_reply,
                'form_url': form_url,
                'reply_form': reply_form,
                'back_url': back_url,
                'moderator': moderator,
                'subscribed': subscribed,
                'replies': replies,
                'highlight_word': highlight_word,
                'poll': poll,
                'poll_form': poll_form,
                })
    else:
        return render(request, 'forums/lofi/thread.html', {'categories': Category.objects.all(),
                'thread': thread,
                'replies': replies,
                'poll': poll,
                'poll_form': poll_form,
                })


@login_required
@transaction.commit_on_success
def add_thread(request, forum_id):
    """
    create a new thread, with or without poll
    """
    forum = get_object_or_404(Forum, pk=forum_id)
    if not forum.category.has_access(request.user):
        return HttpResponseForbidden()

    ip = request.META.get('REMOTE_ADDR', None)
    reply_form_kwargs = {"forum":forum, "user":request.user, "ip":ip, }

    if request.method == 'POST':
        form = AddReplyForm(request.POST, request.FILES, **reply_form_kwargs)
        if form.is_valid():
            all_valid = True
        else:
            all_valid = False

        poll_form = PollForm(request.POST)
        create_poll = poll_form.create_poll()
        if not create_poll:
            # All poll fields are empty: User didn't want to create a poll
            # Don't run validation and remove all form error messages
            poll_form = PollForm() # create clean form without form errors
        elif not poll_form.is_valid():
            all_valid = False

        if all_valid:
            reply = form.save()
            if create_poll:
                poll_form.save(reply)
                messages.success(request, _("Thread with poll saved."))
            else:
                messages.success(request, _("Thread saved."))
            return HttpResponseRedirect(reply.get_absolute_url())
    else:
        form = AddReplyForm(
            initial={
                'markup': request.user.forum_profile.markup,
                'subscribe': request.user.forum_profile.auto_subscribe,
            },
            **reply_form_kwargs
        )
        if forum_id: # Create a new thread
            poll_form = PollForm()

    context = {
        'forum': forum,
        'create_poll_form': poll_form,
        'form': form,
        'form_url': request.path,
        'back_url': forum.get_absolute_url(),
    }
    return render(request, 'forums/add_thread.html', context)


@transaction.commit_on_success
def upload_avatar(request, username, template=None, form_class=None):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated() and user == request.user or request.user.is_superuser:
        form = build_form(form_class, request, instance=user.forum_profile)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, _("Your avatar uploaded."))
            return HttpResponseRedirect(reverse('forums:forum_profile', args=[user.username]))
        return render(request, template, {'form': form,
                'avatar_width': defaults.AVATAR_WIDTH,
                'avatar_height': defaults.AVATAR_HEIGHT,
               })
    else:
        thread_count = Thread.objects.filter(user__id=user.id).count()
        if user.forum_profile.reply_count < defaults.POST_USER_SEARCH and not request.user.is_authenticated():
            messages.error(request, _("Please sign in."))
            return HttpResponseRedirect(reverse('user_signin') + '?next=%s' % request.path)
        return render(request, template, {'profile': user,
                'thread_count': thread_count,
               })



def show_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    count = reply.thread.replies.filter(created_date__lt=reply.created_date).count() + 1
    page = math.ceil(count / float(defaults.TOPIC_PAGE_SIZE))
    url = '%s?page=%d#reply-%d' % (reverse('forums:thread', args=[reply.thread.id]), page, reply.id)
    return HttpResponseRedirect(url)


@login_required
@transaction.commit_on_success
def edit_reply(request, reply_id):
    from filizver.forum.templatetags.forum_extras import forum_editable_by

    reply = get_object_or_404(Reply, pk=reply_id)
    thread = reply.thread
    if not forum_editable_by(reply, request.user):
        messages.error(request, _("No permissions to edit this reply."))
        return HttpResponseRedirect(reply.get_absolute_url())
    form = build_form(EditReplyForm, request, thread=thread, instance=reply)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.updated_by = request.user
        reply.save()
        messages.success(request, _("Reply updated."))
        return HttpResponseRedirect(reply.get_absolute_url())

    return render(request, 'forums/edit_reply.html', {'form': form,
            'reply': reply,
            })


@login_required
@transaction.commit_on_success
def delete_replies(request, thread_id):

    thread = Thread.objects.select_related().get(pk=thread_id)

    if forum_moderated_by(thread, request.user):
        deleted = False
        reply_list = request.POST.getlist('reply')
        for reply_id in reply_list:
            if not deleted:
                deleted = True
            delete_reply(request, reply_id)
        if deleted:
            messages.success(request, _("Reply deleted."))
            return HttpResponseRedirect(thread.get_absolute_url())

    last_reply = thread.replies.latest()

    if request.user.is_authenticated():
        thread.update_read(request.user)

    replies = thread.replies.all().select_related()

    initial = {}
    if request.user.is_authenticated():
        initial = {'markup': request.user.forum_profile.markup}
    form = AddReplyForm(thread=thread, initial=initial)

    moderator = request.user.is_superuser or\
        request.user in thread.forum.moderators.all()
    if request.user.is_authenticated() and request.user in thread.subscribers.all():
        subscribed = True
    else:
        subscribed = False
    return render(request, 'forums/delete_replies.html', {
            'thread': thread,
            'last_reply': last_reply,
            'form': form,
            'moderator': moderator,
            'subscribed': subscribed,
            'replies': replies,
            })


@login_required
@transaction.commit_on_success
def move_thread(request):
    if 'thread_id' in request.GET:
        #if move only 1 thread
        thread_ids = [request.GET['thread_id']]
    else:
        thread_ids = request.POST.getlist('thread_id')
    first_thread = thread_ids[0]
    thread = get_object_or_404(Thread, pk=first_thread)
    from_forum = thread.forum
    if 'to_forum' in request.POST:
        to_forum_id = int(request.POST['to_forum'])
        to_forum = get_object_or_404(Forum, pk=to_forum_id)
        for thread_id in thread_ids:
            thread = get_object_or_404(Thread, pk=thread_id)
            if thread.forum != to_forum:
                if forum_moderated_by(thread, request.user):
                    thread.forum = to_forum
                    thread.save()

        #TODO: not DRY
        try:
            last_reply = Reply.objects.filter(thread__forum__id=from_forum.id).latest()
        except Reply.DoesNotExist:
            last_reply = None
        from_forum.last_reply = last_reply
        from_forum.thread_count = from_forum.threads.count()
        from_forum.reply_count = from_forum.replies.count()
        from_forum.save()
        messages.success(request, _("Thread moved."))
        return HttpResponseRedirect(to_forum.get_absolute_url())

    return render(request, 'forums/move_thread.html', {'categories': Category.objects.all(),
            'thread_ids': thread_ids,
            'exclude_forum': from_forum,
            })


@login_required
@transaction.commit_on_success
def stick_unstick_thread(request, thread_id, action):
    thread = get_object_or_404(Thread, pk=thread_id)
    if forum_moderated_by(thread, request.user):
        if action == 's':
            thread.sticky = True
            messages.success(request, _("Thread marked as sticky."))
        elif action == 'u':
            messages.success(request, _("Sticky flag removed from thread."))
            thread.sticky = False
        thread.save()
    return HttpResponseRedirect(thread.get_absolute_url())


@login_required
@transaction.commit_on_success
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    last_reply = reply.thread.last_reply
    thread = reply.thread
    forum = reply.thread.forum

    if not (request.user.is_superuser or\
        request.user in reply.thread.forum.moderators.all() or \
        (reply.user == request.user and reply == last_reply)):
        messages.success(request, _("You haven't the permission to delete this reply."))
        return HttpResponseRedirect(reply.get_absolute_url())

    reply.delete()
    messages.success(request, _("Reply deleted."))

    try:
        Thread.objects.get(pk=thread.id)
    except Thread.DoesNotExist:
        #removed latest reply in thread
        return HttpResponseRedirect(forum.get_absolute_url())
    else:
        return HttpResponseRedirect(thread.get_absolute_url())


@login_required
@transaction.commit_on_success
def open_close_thread(request, thread_id, action):
    thread = get_object_or_404(Thread, pk=thread_id)
    if forum_moderated_by(thread, request.user):
        if action == 'c':
            thread.closed = True
            messages.success(request, _("Thread closed."))
        elif action == 'o':
            thread.closed = False
            messages.success(request, _("Thread opened."))
        thread.save()
    return HttpResponseRedirect(thread.get_absolute_url())


def users(request):
    users = User.objects.filter(forum_profile__reply_count__gte=defaults.POST_USER_SEARCH).order_by('username')
    form = UserSearchForm(request.GET)
    users = form.filter(users)
    return render(request, 'forums/users.html', {'users': users,
            'form': form,
            })


@login_required
@transaction.commit_on_success
def delete_subscription(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.subscribers.remove(request.user)
    messages.info(request, _("Thread subscription removed."))
    if 'from_thread' in request.GET:
        return HttpResponseRedirect(reverse('forums:thread', args=[thread.id]))
    else:
        return HttpResponseRedirect(reverse('forums:forum_profile', args=[request.user.username]))


@login_required
@transaction.commit_on_success
def add_subscription(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.subscribers.add(request.user)
    messages.success(request, _("Thread subscribed."))
    return HttpResponseRedirect(reverse('forums:thread', args=[thread.id]))


@login_required
def show_attachment(request, hash):
    attachment = get_object_or_404(Attachment, hash=hash)
    file_data = file(attachment.get_absolute_path(), 'rb').read()
    response = HttpResponse(file_data, mimetype=attachment.content_type)
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(attachment.name)
    return response


@login_required
@csrf_exempt
def reply_preview(request):
    '''Preview for markitup'''
    markup = request.user.forum_profile.markup
    data = request.POST.get('data', '')

    data = convert_text_to_html(data, markup)
    if defaults.SMILES_SUPPORT:
        data = smiles(data)
    return render(request, 'forums/reply_preview.html', {'data': data})
