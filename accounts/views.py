from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
# from django.contrib.auth.models import User
from .models import CustomUser
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from django.contrib.messages.views import SuccessMessageMixin

from .forms import SignupForm, ProfileForm

class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

class ProfileEditView(UpdateView):
    model = CustomUser
    fields = ('username', 'description', 'photo', )
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Your profile has been updated'
