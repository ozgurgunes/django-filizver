from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from manifest.core.decorators import owner_required

class TopicList(ListView):
    queryset = Post.objects.select_related().all()
    template_name = "posts/post_list.html"
            
class TopicDetail(DetailView):
    queryset = Post.objects.select_related().all()
    template_name = "posts/post_detail.html"
    
    @method_decorator(owner_required(Post))
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetail, self).dispatch(request, *args, **kwargs)
    
class TopicForm(FormView):
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = '/posts'
    
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
