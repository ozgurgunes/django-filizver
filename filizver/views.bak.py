from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from tagging.models import Tag, TaggedItem
from filizver.models import *
from filizver.forms import TopicForm, BranchForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
   
# Create your views here.

@login_required
def homepage(request, **kwargs):
    """
    Lists users and followings topics
    """
    queryset = Topic.objects.for_user(request.user)
    extra_context={'form': TopicForm(initial={'user': request.user})}
    return object_list(request, queryset=queryset, template_name='filizver/home_filizver.html', extra_context=extra_context)


def topic_detail(request, username=None, slug=None, id=None, *args, **kwargs):
    extra_context = {'object': get_object_or_404(Topic, user__username=username, slug=slug, pk=id)}
    extra_context['branch_form'] = BranchForm()
    return render_to_response('filizver/topic_detail.html', extra_context, context_instance=RequestContext(request))

@login_required
def topic_create(request):
    extra_context={'form': TopicForm(initial={'user': request.user})}
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # TODO: Need serious improvements and refactoring below
            topic = form.save()            
            extra_context['created'] = True
            extra_context['object'] = topic 
            return redirect(topic)
        else:
            extra_context = {'form': TopicForm(request.POST)}
    extra_context['user'] = request.user
    return render_to_response('filizver/topic_create.html', extra_context, context_instance=RequestContext(request))

@login_required
def topic_update(request, id=None):
    topic = get_object_or_404(Topic, pk=id)
    if not request.user.has_perm('filizver.change_topic', topic):
        return HttpResponseForbidden(_('User has no permission'))
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            topic = form.save()
            return redirect(topic)
            #return render_to_response('filizver/topic_update.html', {'updated': True, 'form': form, 'user': request.user, 'object': topic}, context_instance=RequestContext(request))
    else:
        errors = data = {}
        form = TopicForm(instance=topic)
    return render_to_response('filizver/topic_update.html', {'form': form, 'user': request.user, 'object': topic}, context_instance=RequestContext(request))

@login_required
def topic_delete(request, id=None):
    topic = get_object_or_404(Topic, pk=id)
    if not request.user.has_perm('filizver.delete_topic', topic):
        return HttpResponseForbidden(_('User has no permission'))
    p = str(topic)
    comments.get_model().objects.filter(content_type__pk=ContentType.objects.get_for_model(Topic).id, object_pk=topic.id).delete()
    topic.delete()
    return redirect('filizver_topic_delete_complete')
    
@login_required
def branch_create(request):
    extra_context={'form': BranchForm(initial={'user': request.user})}
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()            
            extra_context['created'] = True
            extra_context['object'] = branch 
            return redirect(branch.source)
        else:
            extra_context = {'form': BranchForm(request.POST)}
    return render_to_response('filizver/branch_create.html', extra_context, context_instance=RequestContext(request))
    
def branch_delete(request, post_id=None):
    pass

@login_required
def post_create(request, id=None, module=None):
    topic = get_object_or_404(Topic, pk=id)
    if not request.user in topic.user.relationships.following():
        return HttpResponseForbidden(_('User has no permission'))    
    extra_context = { 'module': module, 'topic': topic }
    return render_to_response('filizver/post_create_ajax.html', extra_context, context_instance=RequestContext(request))

@login_required
def post_sort(request, id=None):
    topic = get_object_or_404(Topic, pk=id)
    if not request.user.has_perm('filizver.change_topic', topic):
        return HttpResponseForbidden(_('User has no permission'))
    if request.method == 'POST':
        for position, pk in enumerate(request.POST.getlist('post[]')):
            Post.objects.filter(pk=pk).update(position=position+1)
    extra_context = { 'object': topic }
    return render_to_response('filizver/_topic_posts.html', extra_context, context_instance=RequestContext(request))
        

def topic_tagged(request, tag, template_name='filizver/topic_tagged.html', **kwargs):
    tag                 = tag.replace('-',' ')
    query_tag           = Tag.objects.get(name=tag)
    kwargs['queryset']  = TaggedItem.objects.get_by_model(Topic, query_tag).order_by('-date_created')
    kwargs['extra_context'] = {
        'tag'       : tag,
        'user'      : request.user,
    }
    return object_list(request, template_name=template_name, **kwargs)

def topic_search(request, template_name='filizver/topic_search.html', **kwargs):
    keyword     = request.GET.get('s', '')
    kwargs['queryset'] = Topic.objects.search(keyword)
    kwargs['extra_context'] = {
        'keyword'   : keyword,
        'user'      : request.user,
    }
    return object_list(request, template_name=template_name, **kwargs)
