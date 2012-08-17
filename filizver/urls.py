from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from filizver.models import Topic
from filizver.forms import BranchForm
from filizver import views

urlpatterns = patterns('',
    url(r'^$', views.TopicList.as_view(), None, name='filizver_homepage'),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/(?P<id>\d+)/$', views.TopicDetail.as_view(), name='filizver_topic_detail'),        
    url(r'^create/topic$', views.TopicFormView.as_view(), name='filizver_topic_create'),    
    url(r'^update/topic/(?P<id>\d+)$', views.TopicFormView.as_view(), name='filizver_topic_update'),
#    url(r'^delete/topic/(?P<id>\d+)$', views.TopicDelete.as_view(), name='filizver_topic_delete'),
    url(r'^delete/topic/complete$', TemplateView.as_view(template_name='filizver/topic_delete.html'), name='filizver_topic_delete_complete'),
#    url(r'^sort/posts/(?P<id>\d+)$', views.post_sort, name='filizver_post_sort'),    
    url(r'^create/post/(?P<id>\d+)/(?P<module>[-\w]+)$', views.PostFormView.as_view(), name='filizver_post_create'),    
    url(r'^create/branch$', views.BranchFormView.as_view(), name='filizver_branch_create'),    
    url(r'^tags/$', TemplateView.as_view(template_name='filizver/topic_tags.html'), name='filizver_topic_tags'),
#    url(r'^tags/(?P<tag>.*)/$', views.topic_tagged, None, name='filizver_topic_tagged'),
#    url(r'^search/$', views.topic_search, None, name='filizver_topic_search'),
)
