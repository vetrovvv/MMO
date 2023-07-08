import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'MMOBoard.settings')

app = Celery('MMOBoard')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()



# заносим таски в очередь
app.conf.beat_schedule = {
    'every': { 
        'task': 'announcements.tasks.weekly_mail',
        'schedule': crontab(day_of_week=0)
    },

}
