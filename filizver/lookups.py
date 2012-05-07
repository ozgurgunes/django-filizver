from django.db import models
from filizver.models import Topic, Branch
from selectable.base import ModelLookup
from selectable.registry import registry

class BranchLookup(ModelLookup):
    model   = Topic
    search_fields = ['title__icontains',]
    
    def get_query(self,request,q):
        """
        Return a query set.  you also have access to request.user if needed
        
        """
        topic_id = request.GET.get('topic_id', None)
        branches_qs = Branch.objects.filter(topic__pk=topic_id).values('source')
        return Topic.objects.exclude(pk=topic_id).exclude(pk__in=branches_qs).filter(
                                models.Q(title__istartswith=q) | models.Q(slug__istartswith=q))

    def format_result(self,topic):
        # The search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return u"%s, %s" % (topic.user, topic.date_created)

    def format_item(self,topic):
        # The display of a currently selected object in the area below the search box. html is OK """
        return unicode(topic)

    def get_objects(self,ids):
        # Given a list of ids, return the objects ordered as you would like them on the admin page.
        # This is for displaying the currently selected items (in the case of a ManyToMany field)
        return Topic.objects.filter(pk__in=ids).order_by('title','-date_created')

registry.register(BranchLookup)
