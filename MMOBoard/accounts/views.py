from django.contrib.auth.models import User
from django.views.generic import CreateView,View,DetailView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/announcements/'

# class ProfileView(DetailView):
#     model = AnnouncementAuthor
#     context_object_name = 'profile'
#     template_name = 'accounts/profile.html'
#
#
