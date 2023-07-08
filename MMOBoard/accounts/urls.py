from django.urls import path

from .views import BaseRegisterView
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('accounts/',
         BaseRegisterView.as_view(template_name='accounts/base.html'),name='signup'),
]