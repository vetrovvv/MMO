
from django.views.generic import  DetailView,ListView,CreateView,UpdateView,DeleteView
from .filters import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect,render,reverse

from django.core.cache import cache
from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

class AnnouncementList(ListView):

    model = Announcement
    context_object_name = 'announcements'
    ordering = ['-created_at_date']
    template_name = 'announcements/announcements.html'
    paginate_by = 5
    form_class = SubscribeCategoryForm


    def get_queryset(self):
        queryset = AnnouncementFilter(self.request.GET, super().get_queryset()).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscribeCategoryForm()

        return context






class AddAnnouncement(LoginRequiredMixin,CreateView):
    model = Announcement
    template_name = 'announcements/add.html'
    form_class = AnnouncementForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnnouncementForm()
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.announcement_author = Profile.objects.get(profile = request.user.id)
            saved_form = form.save()
            files = request.FILES.getlist('files')
            for f in files:
                a = Files(file=f)
                a.save()
                saved_form.files.add(a)
        return redirect('/announcements/')





class Search(ListView):
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'announcements/search.html'
    ordering = ['-created_at_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = AnnouncementFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = AnnouncementFilter(self.request.GET, queryset=self.get_queryset())
        filter_qs =filter.qs
        paginator = Paginator(filter_qs,5)
        page = self.request.GET.get('page',1)
        try:
            announcements = paginator.page(page)
        except PageNotAnInteger:
            announcements = paginator.page(1)
        except EmptyPage:
            announcements = paginator.page(paginator.num_pages)
        context['paginator']= paginator
        context['announcements']= announcements
        return context

class AnnouncementUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('announcements.change_announcement',
                           )
    model = Announcement
    template_name = 'announcements/announcement_update.html'
    form_class = AnnouncementForm

    def get_object(self, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        obj = Announcement.objects.get(pk=id)
        if obj.announcement_author_id == user.id:
            return obj
        else:
            raise PermissionDenied()

class AnnouncementDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Announcement
    permission_required = ('announcements.delete_announcement',
                           )
    template_name = 'announcements/announcement_delete.html'
    success_url = '/announcements/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        announcement = Announcement.objects.get(pk=id)
        if announcement.announcement_author.id == self.request.user.id:
            return Announcement.objects.get(pk=id)
        else:
            raise PermissionDenied()


class AnnouncementDetail(LoginRequiredMixin,DetailView):
    model = Announcement
    template_name = 'announcements/announcement.html'
    context_object_name = 'announcement'

    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context[
            'value1'] = self.object.announcement_author
        context[
            'object'] = self.object
        context[
            'user'] = Profile.objects.get(profile=self.request.user)
        return context

    def get_object(self,*args,**kwargs):
        obj = cache.get(f'announcement-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'announcement-{self.kwargs["pk"]}', obj)
        return obj






class ProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'announcements/profile.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        obj = Profile.objects.get(id=id)
        return obj




    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        author = Profile.objects.get(profile=self.request.user.id)
        count_responses = len(ANCTResponse.objects.filter(author=author,confirm=False,refuse=False))
        context[
            'userprofile'] = author
        context[
            'count_responses'] = count_responses

        return context




class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model =Profile
    context_object_name = 'profile'
    template_name = 'announcements/profile_update.html'
    form_class = ProfileUpdateForm

    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        author = Profile.objects.get(profile=self.request.user.id)
        context[
            'userprofile'] = author

        return context

    def get_object(self, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        obj = Profile.objects.get(pk=id)
        if obj.id == user.id:
            return obj
        else:
            raise PermissionDenied()





class AnnouncementsProfileListView(ListView,LoginRequiredMixin):
    model = Announcement
    context_object_name = 'announcements_profile'
    template_name = 'announcements/announcements_profile_list_view.html'

    def get_queryset(self):
        user = Profile.objects.get(profile=self.request.user)
        queryset = Announcement.objects.filter(announcement_author=user)
        return queryset



class ANCTResponseProfileListView(ListView,LoginRequiredMixin):
    model = ANCTResponse
    template_name = 'announcements/response_list_profile.html'
    context_object_name = 'responses'
    ordering = ['-created_at_date']
    paginate_by = 5

    # def get_queryset(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     profile = Profile.objects.get(id=pk)
    #     queryset = profile.author.all().order_by('id')
    #     return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = ANCTResponseFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = ANCTResponseFilter(self.request.GET, queryset=self.get_queryset())
        filter_qs = filter.qs
        paginator = Paginator(filter_qs,5)
        page = self.request.GET.get('page',1)
        try:
            responses = paginator.page(page)
        except PageNotAnInteger:
            responses = paginator.page(1)
        except EmptyPage:
            responses = paginator.page(paginator.num_pages)
        context['paginator']= paginator
        context['responses']= responses
        return context



class ANCTResponseListView(ListView,LoginRequiredMixin,PermissionRequiredMixin):
    model = ANCTResponse
    template_name = 'announcements/response_list_announcement.html'
    context_object_name = 'responses'

    def get_queryset(self,*args, **kwargs):
        pk = self.kwargs.get('pk')
        an = Announcement.objects.get(id=pk)
        queryset = ANCTResponse.objects.filter(announcement=an)
        if self.request.user.id == an.announcement_author.id:
            return queryset
        else:
            raise PermissionDenied()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        announcement = Announcement.objects.get(id=pk)
        context[
            'announcement'] = announcement

        return context

class ANCTResponseDetailView(DetailView, LoginRequiredMixin,PermissionRequiredMixin):
    model = ANCTResponse
    template_name = 'announcements/response_announcement_detail.html'
    context_object_name = 'response'
    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = ANCTResponse.objects.get(id=id)
        if obj.author.id == self.request.user.id:
            return obj
        else:
            raise PermissionDenied()




    # def post(self, request,pk, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     an = Announcement.objects.get(id=pk)
    #     if form.is_valid():
    #         obj = form.save(commit=False)
    #         obj.buyer = AnnouncementAuthor.objects.get(announcement_author=request.user.id)
    #         obj.author = an.announcement_author
    #         obj.announcement = an
    #         form.save()
    #
    #     return redirect('/announcements/')

    # def get_object(self,*args,**kwargs):
    #     user = self.request.user
    #     obj = cache.get(f'anctresponse-{self.kwargs["pk"]}', None)
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'anctresponse-{self.kwargs["pk"]}', obj)
    #         if obj.buyer.id == user.id or obj.announcement.announcement_author.id == user.id:
    #             return obj
    #         else:
    #             raise PermissionDenied()





@login_required
def become_subscriber(request):
    if request.method == 'POST':
        form = SubscribeCategoryForm(request.POST)
        if form.is_valid():
            category = request.POST.get("category")
            sub = Profile.objects.get(profile=request.user)
            category_addsub = Category.objects.get(pk=category)
            category_addsub.subscribers.add(sub)
            category_addsub.save()
    return redirect('/announcements/')

@login_required
def become_subscriber_detail(request):
    categories = request.POST.getlist('category')
    sub = Profile.objects.get(profile=request.user)
    for category in categories:
        category_addsub = Category.objects.get(id=category)
        category_addsub.subscribers.add(sub)
        category_addsub.save()
    return redirect('/announcements/')



def redirect_view(request):
    response = redirect('http://127.0.0.1:8000/accounts/login/')
    return response

@login_required
def redir(request):
    user = Profile.objects.get(profile=request.user)
    if user.email_confirmed is False:
        return redirect('/announcements/confirm')

@login_required
def response_announcement(request):
    if request.method == 'POST':
        author = Profile.objects.get(id=request.POST.get('author'))
        announcement = Announcement.objects.get(id=request.POST.get('announcement'))
        message = request.POST.get('message')
        buyer = Profile.objects.get(profile=request.user)
        ANCTResponse.objects.create(author=author,buyer=buyer,announcement=announcement,message=message)
    return redirect('/announcements/')

@login_required
def unsubscribe(request,**kwargs):
    id = kwargs.get('pk')
    profile = Profile.objects.get(id=id)

    if request.method == 'POST':
        categories = request.POST.getlist('category')
        for category in categories:
            cat = Category.objects.get(category=category)
            cat.subscribers.remove(profile)

    return redirect('/announcements/')


@login_required
def confirm(request):
    if request.method == 'POST':
        response = request.POST.get('response')
        obj = ANCTResponse.objects.get(id=response)
        obj.confirm = True
        obj.save()
        return redirect('/announcements/')


@login_required
def refuse(request):
    if request.method == 'POST':
        response = request.POST.get('response')
        obj = ANCTResponse.objects.filter(id=response)
        obj.update(refuse=True)
        obj.first().delete()
        return redirect('/announcements/')



