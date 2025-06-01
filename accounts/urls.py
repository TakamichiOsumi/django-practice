from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import SignupView, ProfileEditView, ProfileDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/',  LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name = 'edit'),
    path('detail/<int:pk>', ProfileDetailView.as_view(), name = 'detail'),
]
