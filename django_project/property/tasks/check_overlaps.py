from celery import shared_task


@shared_task(name='property_check_overlaps_each_other')
def property_check_overlaps_each_other():
    pass
