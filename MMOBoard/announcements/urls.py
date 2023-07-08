from django.urls import path,re_path,include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', AnnouncementList.as_view(),name='announcements'),
    path('<int:pk>',AnnouncementDetail.as_view(),name='announcement'),
    path('<int:pk>/responses/',ANCTResponseListView.as_view(),name='response_list'),
    path('search/', Search.as_view(),name='search'),
    path('add/', AddAnnouncement.as_view(),name='add'),
    path('<int:pk>/edit/',AnnouncementUpdateView.as_view(),name='edit'),
    path('<int:pk>/delete/',AnnouncementDeleteView.as_view(),name='delete'),
    path('login/',redirect_view,name='login'),
    path('become_subscriber/',become_subscriber,name = "become_subscriber"),
    path('become_subscriber_detail/',become_subscriber_detail,name = "become_subscriber_detail"),
    path('profile/<int:pk>/',ProfileView.as_view(),name = "profile"),
    path('profile/<int:pk>/update/',ProfileUpdateView.as_view(),name = "update_profile"),
    path('profile/<int:pk>/responses/',ANCTResponseProfileListView.as_view(),name = "profile_responses"),
    path('profile/<int:pk>/responses/<int:id>',ANCTResponseDetailView.as_view(),name = "detail_response"),
    path('confirm_response/',confirm,name = "confirm_response"),
    path('refuse_response/',refuse,name = "refuse_response"),
    path('confirm_profile/',redir,name = "confirm_profile"),
    # path('myannouncements'+'/responses/<int:pk>',ANCTResponseDetailView.as_view(),name = "anctdetail"),
    path('response/',response_announcement,name = "response"),
    path('profile/<int:pk>/unsubscribe/',unsubscribe,name = "unsubscribe"),



]