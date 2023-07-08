
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
today = timezone.now

from django.core.cache import cache

from urllib.parse import unquote



def get_image_path(instance, filename):
    return os.path.join(str(instance.id), filename)

def get_av_path(instance, filename):
   return os.path.join('avatars/',str(instance.profile.pk),f"{filename}")

class Profile(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile',unique=True,verbose_name="Пользователь")
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=get_av_path,blank=True, null=True,verbose_name='Аватар')


    def __str__(self):
        return self.profile.username
    def get_my_responses_url(self):
        return f'/announcements/profile/{self.id}/responses/'
    def get_absolute_url(self):
        return f'/announcements/profile/{self.id}'

    def get_update_url(self):
        return f'/announcements/profile/{self.id}/update/'


    def not_subscribed_categories(self):
        return Category.objects.filter().exclude(subscribers=self)

    def subscribed_categories_len(self):
        return len(Category.objects.filter(subscribers=self))

    def not_subscribed_categories_len(self):
        return len(Category.objects.filter().exclude(subscribers=self))

    def get_all_categories(self):
        return Category.objects.all()





class Category(models.Model):
    category = models.CharField(max_length = 200,unique=True,verbose_name="Категория")
    subscribers = models.ManyToManyField(Profile,related_name="subscribing_categories",blank=True)
    def __str__(self):
        return self.category.title()

class Announcement(models.Model):
    announcement_author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='author_announcements',verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)
    created_at_date = models.DateField(auto_now_add=True,verbose_name="Дата публикации")
    header = models.CharField(default="",max_length=64,verbose_name="Заголовок")
    main_text = models.TextField(default="",verbose_name="Текст объявления")
    category = models.ManyToManyField(to='Category',through='AnnouncementCategory',verbose_name="Категория")






    def __str__(self):
        l = self.announcement_author.profile.username
        time = self.created_at.strftime("%d:%m:%Y:%H:%M")
        return f'Автор {l}:={self.header.title()}{self.main_text}{time}'

    def get_response_url(self):
        return f'/announcements/{self.id}/responses/'


    def get_absolute_url(self):
        return f'/announcements/{self.id}'

    def get_self_categories(self):
        return list(self.category.all())




    def get_first_photo_href(self):
        extensions = ['.jpg','.jpeg','.png']
        for file in self.files.all():
            if file is not None and file.extension() in extensions:
                return file.file_url



    def preview(self):
        return self.main_text[0:124] + "..."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'announcement-{self.pk}')

class Files(models.Model):
    file = models.FileField(upload_to="files/",blank=True)
    announcement = models.ManyToManyField(Announcement,related_name="files")

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    @property
    def file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return unquote(self.file.url)

class AnnouncementCategory(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE,related_name="announcement_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="categories_of_announcements")





class ANCTResponse(models.Model):
    author = models.ForeignKey(Profile,related_name='author',on_delete=models.CASCADE,default=None)
    announcement = models.ForeignKey(Announcement,related_name='anctresponses',on_delete=models.CASCADE,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(Profile,related_name='buyers',on_delete=models.CASCADE,default=None)
    message = models.TextField(default="")
    confirm = models.BooleanField(default=False)
    refuse = models.BooleanField(default=False)



