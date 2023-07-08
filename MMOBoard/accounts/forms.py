from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Users_group = Group.objects.get(name='Users')
        Users_group.user_set.add(user)
        return user
