from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post, Like
from .consts import POST_PER_PAGE

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'timeline/index.html'
    pginate_by = 10
    posts = Post.objects.order_by('-created_at')

    def get_queryset(self):
        return self.posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.posts

        paginator = Paginator(self.posts, POST_PER_PAGE)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.page(page_number)
        context['page_obj'] = page_obj
        return context

class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'timeline/create.html'
    success_url = reverse_lazy('timeline:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        messages.success(self.request, 'Posted')
        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request,
                             messages.WARNING,
                             form.errors)
        return redirect('timeline:index')

class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('timeline:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            messages.success(self.request, 'Removed')
            return super().delete(request, *args, **kwargs)

class LikeView(LoginRequiredMixin, generic.View):
    model = Like
    success_url = reverse_lazy('timeline:index')

    def post(self, request, *args, **kwargs):
        post_id = kwargs["pk"]
        post = Post.objects.get(id = post_id)
        if Like.objects.filter(user = self.request.user,
                               post = post).exists():
            print(f'{self.request.user} already liked the post {post_id}.')
        else:
            like = Like(user = self.request.user, post = post)
            like.save()
            print(f'{self.request.user} liked post No. {post_id}.')

        return redirect('timeline:index')

index = IndexView.as_view()
create = CreateView.as_view()
delete = DeleteView.as_view()
like = LikeView.as_view()
