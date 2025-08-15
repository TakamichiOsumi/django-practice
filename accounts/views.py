from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import CustomUser, Connection
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import SignupForm, ProfileForm

class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:detail')

    def get_success_url(self):
        return reverse('accounts:detail',
                       kwargs = { 'pk': self.object.pk })

class ProfileEditView(LoginRequiredMixin,
                      SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = ('username', 'description', 'photo', )
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('accounts:detail')
    success_message = 'Your profile has been updated'

    def get_success_url(self):
        return reverse_lazy('timeline:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        connections = Connection.objects
        users = CustomUser.objects

        # Get the ids of users whom I follow.
        following_conns = connections.filter(following = self.request.user)
        context['following_list'] = users.filter(id__in = [following_conns.values('followed_id')])

        # Get the ids of users who follow me.
        followed_conns = connections.filter(followed = self.request.user)
        context['followed_list'] = users.filter(id__in = [followed_conns.values('following_id')])

        return context

class ProfileDetailView(LoginRequiredMixin,
                        generic.DetailView):
    model = CustomUser
    template_name = 'accounts/detail.html'
    success_url = reverse_lazy('accounts:detail')

    def get_success_url(self):
        return reverse('accounts:detail',
                       kwargs = { 'pk': self.object.pk })

    def post(self, request, *args, **kwargs):
        followed_user_id = kwargs['pk']
        users = CustomUser.objects
        if users.filter(id = self.request.user.id).exists() and users.filter(id = followed_user_id).exists():
            followed_user = users.get(id = followed_user_id)
            print(f'user = "{self.request.user.username}" followed another user = "{followed_user.username}"')
            if Connection.objects.filter(following = self.request.user,
                                         followed = followed_user).exists():
                print('this combination of follow relationship already exists')
            else:
                new_conn = Connection(following = self.request.user,
                                      followed = followed_user)
                new_conn.save()

        return redirect('timeline:index')

detail = ProfileDetailView.as_view()
