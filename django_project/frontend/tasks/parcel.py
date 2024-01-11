from celery import shared_task
from celery.utils.log import get_task_logger
from frontend.models.base_task import ERROR


logger = get_task_logger(__name__)


@shared_task(name="clear_uploaded_boundary_files")
def clear_uploaded_boundary_files():
    from datetime import datetime, timedelta
    from frontend.models.boundary_search import (
        BoundaryFile, BoundarySearchRequest
    )
    # delete after 3months
    datetime_filter = datetime.now() - timedelta(days=90)
    old_files = BoundaryFile.objects.filter(
        upload_date__lt=datetime_filter
    )
    session_list = []
    for old_file in old_files:
        if old_file.session not in session_list:
            session_list.append(old_file.session)
    old_files.delete()
    BoundarySearchRequest.objects.filter(
        session__in=session_list
    ).delete()


@shared_task(name='boundary_files_search')
def boundary_files_search(request_id):
    from frontend.models.boundary_search import BoundarySearchRequest
    from frontend.utils.upload_file import search_parcels_by_boundary_files
    search_request = BoundarySearchRequest.objects.get(id=request_id)
    try:
        search_parcels_by_boundary_files(search_request)
    except Exception as ex:
        logger.error(f'Failed to process boundary search id {search_request.id}')
        logger.error(ex)
        search_request.status = ERROR
        search_request.errors = str(ex)
        search_request.save(update_fields=['status', 'errors'])


@shared_task(name='patch_parcel_sources')
def patch_parcel_sources():
    from property.models import Parcel
    from frontend.utils.parcel import find_layer_by_cname
    parcels = Parcel.objects.filter(
        source__isnull=True
    )
    logger.info(f'Patch parcels {parcels.count()}')
    for parcel in parcels:
        layer, parcel_id = find_layer_by_cname(parcel.sg_number)
        parcel.source = layer
        parcel.source_id = parcel_id
        parcel.save(update_fields=['source', 'source_id'])
    logger.info(f'Finished patching parcels {parcels.count()}')
