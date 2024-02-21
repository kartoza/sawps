from django.test import TestCase
from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask
)
from core.celery import create_scheduler_task


class FrontendConfigTestCase(TestCase):

    def test_create_scheduler_task(self):
        create_scheduler_task('clear_uploaded_boundary_files',
                              'Clear Uploaded Boundary Files', 30, 'DAYS')
        task = PeriodicTask.objects.get(task='clear_uploaded_boundary_files')
        self.assertEqual(task.interval.every, 30)
        self.assertEqual(task.interval.period, IntervalSchedule.DAYS)
        create_scheduler_task('clear_uploaded_boundary_files',
                              'Clear Uploaded Boundary Files', 2, 'HOURS')
        task.refresh_from_db()
        self.assertEqual(task.interval.every, 2)
        self.assertEqual(task.interval.period, IntervalSchedule.HOURS)
