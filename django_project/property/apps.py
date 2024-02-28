from django.apps import AppConfig
from importlib import import_module


class PropertryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'property'

    def ready(self):
        create_scheduler_task = (
            import_module('core.celery').create_scheduler_task
        )
        create_scheduler_task(
            'property_check_overlaps_each_other',
            'Property check overlaps each other',
            1,
            'DAYS'
        )
