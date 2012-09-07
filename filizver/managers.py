# -*- coding: utf-8 -*-
import operator
from django.db import models
#from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from relationships.utils import positive_filter

class TopicManager(models.Manager):
    """
    Topic manager
    
    def get_query_set(self):
        # Get active objects only everytime.
        return super(TopicManager,  self).get_query_set().filter(is_public=True)

    """        

    def for_user(self, user):
        user_list = User.objects.filter(username=user.username) | user.relationships.following()
        return positive_filter(super(TopicManager, self).all(), user_list)

    def search(self, search_terms):
        from libs.search import normalize
        terms = normalize(search_terms)
        q_objects = []
        
        for term in terms:
            q_objects.append(models.Q(title__icontains=term))
            q_objects.append(models.Q(description__icontains=term))
            q_objects.append(models.Q(tags__icontains=term))
        
        # Start with a bare QuerySet
        qs = self.get_query_set()
        
        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))

# class BranchLookup(ModelLookup):
#     def get_query(self,q,request):
#         """
#         Return a query set.  you also have access to request.user if needed
#         
#         """
#         topic_id = request.GET.get('topic_id', None)
#         branches_qs = Branch.objects.filter(topic__pk=topic_id).values('source')
#         return Topic.objects.exclude(pk=topic_id).exclude(pk__in=branches_qs).filter(models.Q(title__istartswith=q) | models.Q(slug__istartswith=q))
# 
#     def format_result(self,topic):
#         # The search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
#         return u"%s, %s" % (topic.user, topic.date_created)
# 
#     def format_item(self,topic):
#         # The display of a currently selected object in the area below the search box. html is OK """
#         return unicode(topic)
# 
#     def get_objects(self,ids):
#         # Given a list of ids, return the objects ordered as you would like them on the admin page.
#         # This is for displaying the currently selected items (in the case of a ManyToMany field)
#         return Topic.objects.filter(pk__in=ids).order_by('title','-date_created')
# 

# class PostManager(models.Manager):
#     """
#     Managers for the Filizver Post model
#     """
#     def __init__(self):
#         super(PostManager, self).__init__()
#         self.models_by_name = {}
# 
#     def get_for_model(self, model):
#         """
#         Return a QuerySet of only items of a certain type.
#         """
#         return self.filter(content_type=ContentType.objects.get_for_model(model))
# 
#     def get_last_update_of_model(self, model, **kwargs):
#         """
#         Return the last time a given model's items were updated. Returns the epoch if the items were never updated.
#         """
#         qs = self.get_for_model(model)
#         if kwargs:
#             qs = qs.filter(**kwargs)
#         try:
#             return qs.order_by('-date_created')[0].date_created
#         except IndexError:
#             return datetime.fromtimestamp(0)
# 