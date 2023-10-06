from celery import shared_task


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
