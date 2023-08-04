import csv
import logging
from celery import shared_task
from frontend.models import UploadSpeciesCSV
from property.models import (
    PropertyType,
    Province,
    Property
)
from species.models import Taxon, OwnedSpecies
from population_data.models import CountMethod

logger = logging.getLogger('sawps')


@shared_task(name='upload_species_data')
def upload_species_data(upload_session_id):
    try:
        upload_session = UploadSpeciesCSV.objects.get(id=upload_session_id)
    except UploadSpeciesCSV.DoesNotExist:
        logger.error("upload session doesn't exist")
        return

    encoding = 'utf-8-sig'

    with open(upload_session.process_file.path, encoding=encoding
              ) as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        data = list(reader)

        for row in data:

            # save PropertyType
            property_type = PropertyType.objects.get_or_create(
                name=row["Property_type"]
            )

            # save Province
            province = Province.objects.get_or_create(
                name=row["State_province"]
            )

            # Save Property
            property = Property.objects.get_or_create(
                name=row["Property_name"],
                owner_email=row["Owner_email"],
                province=province,
                property_type=property_type,
                property_size_ha=row["PropertySize_verbatim_ha"]
            )

            # Save Taxon
            taxon = Taxon.objects.get_or_create(
                scientific_name=row["Scientific_name"],
                common_name_varbatim=row["Common_name_verbatim"],
            )

            # Save CountMethod
            count_methode = CountMethod.objects.get_or_create(
                name=row["CountMethod_verbatim"]
            )

            # Save OwnedSpecies

            owned_species = OwnedSpecies.objects.get_or_create(
                taxon=taxon,
                count_method=count_methode,
                user=upload_session.uploader,

            )

            upload_session.processed = True

            if not success_response:
                success_response += 'No new data added or updated.'

            upload_session.success_notes = (
                success_response
            )
            upload_session.save()
