from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
     class Meta:
         model = CustomUser
         fields = ("username", )

class ProfileForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
          super(ProfileForm, self).__init__(*args, **kwargs)
          for field in self.fields.values():
               field.widget.attrs['class'] = 'form-control'

     class Meta:
          model = CustomUser
          fields = ('username',)
          help_texts = { 'password' : None }
