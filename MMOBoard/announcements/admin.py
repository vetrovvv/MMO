from django.contrib import admin
from .models import Announcement,Profile,Category,AnnouncementCategory,Files,ANCTResponse


admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(AnnouncementCategory)
admin.site.register(Files)
admin.site.register(ANCTResponse)
