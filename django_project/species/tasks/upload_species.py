# -*- coding: utf-8 -*-

import logging

from celery import shared_task
from frontend.models import UploadSpeciesCSV
from species.scripts.data_upload import SpeciesCSVUpload

logger = logging.getLogger('sawps')


@shared_task(name='upload_species_data')
def upload_species_data(upload_session_id):
    """Task for upload species file in the backend.

    :param
    upload_session_id: Id of upload session model
    :type
    upload_session_id: int
    """

    try:
        upload_session = UploadSpeciesCSV.objects.get(id=upload_session_id)
    except UploadSpeciesCSV.DoesNotExist:
        logger.error("upload session doesn't exist")
        return

    encoding = 'utf-8-sig'

    upload_session.progress = 'Processing'
    upload_session.save()
    file_upload = SpeciesCSVUpload()
    file_upload.upload_session = upload_session
    file_upload.start(encoding)
