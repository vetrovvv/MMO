from MMOBoard.celery import app
import datetime
from announcements.models import *
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives
from MMOBoard import settings

@app.task
def weekly_mail():
    today = datetime.now()
    last_week = today - datetime.timedelta(days=7)
    for cat in Category.objects.all():
        subscribers = set(Profile.objects.filter(subscribing_categories=cat))
        announcements = Announcement.objects.filter(created_at__gte=last_week, category__id=cat.id)
        for u in subscribers:
            html_content = render_to_string(
                'announcements/weekly_message.html',
                {
                    'cat': cat,
                    'announcements': announcements,
                    'link': 'http://127.0.0.1:8000',
                    'user': u.profile,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"Недельная сводка новостей",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[u.profile.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()