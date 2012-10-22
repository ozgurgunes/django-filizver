from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.http import Http404

from filizver.forum.models import Reply, Thread, Forum, Category

class ForumFeed(Feed):
    feed_type = Atom1Feed

    def link(self):
        return reverse('forum:index')

    def item_guid(self, obj):
        return str(obj.id)

    def item_pubdate(self, obj):
        return obj.created

    def item_author_name(self, item):
        return item.user.username


class LastReplies(ForumFeed):
    title = _('Latest posts on forum')
    description = _('Latest posts on forum')
    title_template = 'djangobb_forum/feeds/posts_title.html'
    description_template = 'djangobb_forum/feeds/posts_description.html'

    def get_object(self, request):
        user_groups = request.user.groups.all()
        if request.user.is_anonymous():
            user_groups = []
        allow_forums = Forum.objects.filter(
                Q(category__groups__in=user_groups) | \
                Q(category__groups__isnull=True))
        return allow_forums

    def items(self, allow_forums):
        return Reply.objects.filter(topic__forum__in=allow_forums).order_by('-created')[:15]


class LastThreads(ForumFeed):
    title = _('Latest topics on forum')
    description = _('Latest topics on forum')
    title_template = 'djangobb_forum/feeds/topics_title.html'
    description_template = 'djangobb_forum/feeds/topics_description.html'

    def get_object(self, request):
        user_groups = request.user.groups.all()
        if request.user.is_anonymous():
            user_groups = []
        allow_forums = Forum.objects.filter(
                Q(category__groups__in=user_groups) | \
                Q(category__groups__isnull=True))
        return allow_forums

    def items(self, allow_forums):
        return Thread.objects.filter(forum__in=allow_forums).order_by('-created')[:15]


class LastRepliesOnThread(ForumFeed):
    title_template = 'djangobb_forum/feeds/posts_title.html'
    description_template = 'djangobb_forum/feeds/posts_description.html'
    
    def get_object(self, request, topic_id):
        topic = Thread.objects.get(id=topic_id)
        if not topic.forum.category.has_access(request.user):
            raise Http404
        return topic

    def title(self, obj):
        return _('Latest posts on %s topic' % obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return _('Latest posts on %s topic' % obj.name)

    def items(self, obj):
        return Reply.objects.filter(topic__id=obj.id).order_by('-created')[:15]


class LastRepliesOnForum(ForumFeed):
    title_template = 'djangobb_forum/feeds/posts_title.html'
    description_template = 'djangobb_forum/feeds/posts_description.html'

    def get_object(self, request, forum_id):
        forum = Forum.objects.get(id=forum_id)
        if not forum.category.has_access(request.user):
            raise Http404
        return forum

    def title(self, obj):
        return _('Latest posts on %s forum' % obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return _('Latest posts on %s forum' % obj.name)

    def items(self, obj):
        return Reply.objects.filter(topic__forum__id=obj.id).order_by('-created')[:15]


class LastRepliesOnCategory(ForumFeed):
    title_template = 'djangobb_forum/feeds/posts_title.html'
    description_template = 'djangobb_forum/feeds/posts_description.html'
    
    def get_object(self, request, category_id):
        category = Category.objects.get(id=category_id)
        if not category.has_access(request.user):
            raise Http404
        return category

    def title(self, obj):
        return _('Latest posts on %s category' % obj.name)

    def description(self, obj):
        return _('Latest posts on %s category' % obj.name)

    def items(self, obj):
        return Reply.objects.filter(topic__forum__category__id=obj.id).order_by('-created')[:15]
