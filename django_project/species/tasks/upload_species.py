# -*- coding: utf-8 -*-

import logging

from celery import shared_task
from django.db.models.fields.files import FieldFile
from frontend.models import UploadSpeciesCSV
from species.scripts.data_upload import SpeciesCSVUpload

logger = logging.getLogger('sawps')


def try_delete_uploaded_file(file: FieldFile):
    try:
        file.delete(save=False)
    except Exception:
        logger.error('Failed to delete file!')


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
    upload_session.processed = False
    upload_session.success_notes = None
    upload_session.error_notes = None
    if upload_session.success_file:
        try_delete_uploaded_file(upload_session.success_file)
        upload_session.success_file = None
    if upload_session.error_file:
        try_delete_uploaded_file(upload_session.error_file)
        upload_session.error_file = None
    upload_session.save()
    file_upload = SpeciesCSVUpload()
    file_upload.upload_session = upload_session
    file_upload.start(encoding)
