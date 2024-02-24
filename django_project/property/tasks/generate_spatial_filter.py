from celery import shared_task
import logging


logger = logging.getLogger(__name__)


@shared_task(name='generate_spatial_filter')
def generate_spatial_filter_task(property_id):
    from property.models import Property
    from property.spatial_data import (
        save_spatial_values_from_property_layers
    )

    property_obj = Property.objects.get(
        id=property_id
    )
    save_spatial_values_from_property_layers(
        property_obj
    )


@shared_task(name='generate_spatial_filter_for_all_properties')
def generate_spatial_filter_for_all_properties():
    from property.models import Property
    from property.spatial_data import (
        save_spatial_values_from_property_layers
    )

    properties = Property.objects.all().order_by('id')
    logger.info(
        f'Generating spatial filter for {properties.count()} properties.')
    for property in properties.iterator(chunk_size=1):
        save_spatial_values_from_property_layers(
            property
        )
    logger.info(
        'Finished generating spatial filter '
        f'for {properties.count()} properties.')
