from django.forms import ModelForm,TextInput,FileInput,HiddenInput,PasswordInput,formset_factory
from .models import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement

        fields = ['header', 'main_text','category']
        widgets = {
            'announcement_author': TextInput(),
        }
class FileForm(ModelForm):
    class Meta:
        model = Files
        fields = ['file']
        widgets = {
            'announcement': TextInput(),
        }



class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Users_group = Group.objects.get(name='Users')
        Users_group.user_set.add(user)
        return user

class SubscribeCategoryForm(ModelForm):
    class Meta:
        model = AnnouncementCategory
        fields = ['category']

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']




class ResponseForm(ModelForm):
    class Meta:
        model = ANCTResponse
        fields = ['author','announcement','message']






