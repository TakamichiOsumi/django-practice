from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import CustomUser
from django.urls import reverse_lazy, reverse
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

class ProfileDetailView(LoginRequiredMixin,
                        generic.DetailView):
    model = CustomUser
    template_name = 'accounts/detail.html'
    success_url = reverse_lazy('accounts:detail')

    def get_success_url(self):
        return reverse('accounts:detail',
                       kwargs = { 'pk': self.object.pk })

detail = ProfileDetailView.as_view()
