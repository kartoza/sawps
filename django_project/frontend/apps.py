from django.apps import AppConfig
from importlib import import_module


class FrontendConfig(AppConfig):
    name = 'frontend'

    def ready(self):
        create_scheduler_task = (
            import_module('core.celery').create_scheduler_task
        )
        create_scheduler_task('clear_uploaded_boundary_files',
                              'Clear Uploaded Boundary Files', 30, 'DAYS')
        create_scheduler_task('clear_expired_map_session',
                              'clear_expired_map_session', 2, 'HOURS')
        create_scheduler_task('clean_old_model_output',
                              'clean_old_model_output', 30, 'DAYS')
        create_scheduler_task('check_oudated_model_output',
                              'check_oudated_model_output', 1, 'HOURS')
        create_scheduler_task('clean_download_data',
                              'clean_download_data', 2, 'DAYS')
