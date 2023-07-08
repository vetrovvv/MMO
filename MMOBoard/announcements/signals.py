from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from django.contrib.auth.models import User
from .models import Profile,ANCTResponse
from django.template.loader import render_to_string
from MMOBoard import settings
from django.core.mail import send_mail,EmailMultiAlternatives



@receiver(post_save, sender=User)
def user_registered_callback(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(profile=instance)


@receiver(post_save, sender=ANCTResponse)
def response_announcement(sender, instance,created, **kwargs):
    if created:
            announcement = instance.announcement
            instance = instance
            html_content = render_to_string(
                'announcements/response_mail.html',
                {
                'announcement': announcement,
                'instance': instance,
                }
            )
            msg = EmailMultiAlternatives(
            subject=f'Уважаемый {instance.author.profile.username}! На ваше объявление откликнулись!',
            body= 'announcement',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.author.profile.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()



@receiver(post_save, sender=ANCTResponse)
def confirm(sender, instance, **kwargs):
        if instance.confirm is True:
            confirmed_anct = instance.announcement
            html_content = render_to_string(
                'announcements/confirm.html',
                {
                'confirmed_anct': confirmed_anct,
                }
            )
            msg = EmailMultiAlternatives(
            subject=f'Уважаемый {instance.buyer.profile.username}! По вашему откику пришло подтверждение!',
            body="По объявлению: "+str('confirmed_anct'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.buyer.profile.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@receiver(pre_delete,sender=ANCTResponse)
def refuse(sender, instance, **kwargs):
    if instance.confirm is True:
        refused_anct = instance.announcement
        html_content = render_to_string(
            'announcements/refuse.html',
            {
                'refused_anct': refused_anct,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Уважаемый {instance.buyer.profile.username}! Автор объявления отказался от сделки, после одобрения!',
            body='По объявлению: ' + str('refused_anct'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.buyer.profile.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        refused_anct = instance.announcement
        html_content = render_to_string(
            'announcements/refuse.html',
            {
                'refused_anct': refused_anct,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Уважаемый {instance.buyer.profile.username}! Вам пришел отказ по отклику!',
            body='По объявлению: ' + str('refused_anct'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.buyer.profile.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()






