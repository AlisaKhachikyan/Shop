#from __future__ import absolute_import, unicode_literals\

import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_Alisa.settings')

app = Celery('drf_Alisa')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


#app.conf.timezone ='UTC+4'

app.conf.beat_schedule = {
    # Executes every Monday morning at 8:30 a.m.
    'a_weekly_reminder_to_visit': {
        'task': 'Notification.tasks.a_weekly_reminder_to_visit',
        #'schedule': crontab(minute='*/3'),
        'schedule': crontab(hour=8, minute=30, day_of_week=1),
    },
}
