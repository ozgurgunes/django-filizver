from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from filizver.contrib.passages.models import *
from filizver.contrib.passages import views

list_dict = {
    'queryset': Passage.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^(?P<id>[-\w]+)/$',
        view='object_detail',
        kwargs=list_dict,
        name='passages_passage_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=list_dict,
        name='passages_passage_list',
    ),
)

urlpatterns += patterns('',
    url(r'^create/passage/(?P<topic_id>\d+)/$', views.passage_create, name='passages_passage_create'),    
    url(r'^update/passage/(?P<id>\d+)/$', views.passage_update, name='passages_passage_update'),
    url(r'^delete/passage/(?P<id>\d+)/$', views.passage_delete, name='passages_passage_delete'),    
)
