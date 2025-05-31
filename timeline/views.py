from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post

class IndexView(generic.TemplateView):
    template_name = 'timeline/index.html'
    pginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.order_by('-created_at')
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

index = IndexView.as_view()
create = CreateView.as_view()
