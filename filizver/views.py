from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from manifest.core.decorators import owner_required
from manifest.accounts.views import ExtraContextMixin, LoginRequiredMixin

from filizver.models import Topic
from filizver.forms import TopicForm, BranchForm, PostForm

class TopicList(ListView):
    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_list.html"
            
class TopicDetail(DetailView):
    queryset = Topic.objects.select_related().all()
    template_name = "filizver/topic_detail.html"
    
    @method_decorator(owner_required(Topic))
    def dispatch(self, request, *args, **kwargs):
        return super(TopicDetail, self).dispatch(request, *args, **kwargs)
    
class TopicFormView(FormView, LoginRequiredMixin):
    form_class = TopicForm
    template_name = "filizver/topic_form.html"
    success_url = '/topics'
    
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class BranchFormView(FormView, LoginRequiredMixin):
    form_class = BranchForm
    template_name = "filizver/branch_form.html"
    success_url = '/topics'
    
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class PostFormView(FormView, LoginRequiredMixin):
    form_class = BranchForm
    template_name = "filizver/branch_form.html"
    success_url = '/topics'
    
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
