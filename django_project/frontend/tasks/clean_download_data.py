import os
import shutil
from datetime import datetime, timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings


logger = get_task_logger(__name__)


@shared_task(name="clean_download_data", ignore_result=True)
def clean_download_data():
    """
    Clean temporary download data directories after 2 days of creation.

    This job will be run everyday.
    """
    total = 0
    # delete after 7days
    datetime_filter = datetime.now() - timedelta(days=2)
    datetime_filter = datetime_filter.timestamp()
    path = os.path.join(
        settings.MEDIA_ROOT,
        "download_data"
    )
    for path, dirs, files in os.walk(path):
        for dir in dirs:
            dir_path = os.path.join(path, dir)
            mtime = os.stat(dir_path).st_mtime
            if datetime_filter > mtime:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    total += 1
    logger.info(
        f'System cleared {total} temporary download data directories.')
    return total
