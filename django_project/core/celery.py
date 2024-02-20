# -*- coding: utf-8 -*-
"""A celery config for the project.

"""
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = (
    f'redis://default:{os.environ.get("REDIS_PASSWORD", "")}'
    f'@{os.environ.get("REDIS_HOST", "")}',
)

app = Celery('sanbi')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# for scheduling task.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'send-reminder-emails': {
        'task': 'stakeholder.tasks.send_reminder_emails',
        'schedule': crontab(minute='*/5'),  # Run every 5 minute
    },
}


def create_scheduler_task(task_name, task_name_desc,
                          num_interval, interval_schedule):
    """
    Create periodic scheduler tasks.

    :param task_name: task_name
    :param task_name_desc: Name/Description of the task
    :param num_interval: Interval
    :param interval_schedule: one of ['DAYS', 'HOURS']
    """
    from importlib import import_module
    from django.core.exceptions import ValidationError

    schedule = None
    try:
        IntervalSchedule = (
            import_module('django_celery_beat.models').IntervalSchedule
        )

        PeriodicTask = (
            import_module('django_celery_beat.models').PeriodicTask
        )
        if interval_schedule == 'HOURS':
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=num_interval,
                period=IntervalSchedule.HOURS
            )
        elif interval_schedule == 'DAYS':
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=num_interval,
                period=IntervalSchedule.DAYS
            )
    except Exception as e:
        print(e)
        return
    if schedule:
        try:
            PeriodicTask.objects.update_or_create(
                task=task_name,
                defaults={
                    'name': task_name_desc,
                    'interval': schedule
                }
            )
        except ValidationError as e:
            print(e)
