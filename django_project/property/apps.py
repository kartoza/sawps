from django.apps import AppConfig


def create_task_check_overlaps():
    from importlib import import_module
    from django.core.exceptions import ValidationError

    try:
        IntervalSchedule = (
            import_module('django_celery_beat.models').IntervalSchedule
        )

        PeriodicTask = (
            import_module('django_celery_beat.models').PeriodicTask
        )
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS
        )
    except Exception as e:
        print(e)
        return

    try:
        PeriodicTask.objects.update_or_create(
            task='property_check_overlaps_each_other',
            defaults={
                'name': 'Property check overlaps each other',
                'interval': schedule
            }
        )
    except ValidationError as e:
        print(e)


class PropertryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'property'

    def ready(self):
        create_task_check_overlaps()
