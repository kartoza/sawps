import csv
import logging

from activity.models import ActivityType
from celery import shared_task
from frontend.models import UploadSpeciesCSV
from occurrence.models import SurveyMethod
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    CountMethod,
    OpenCloseSystem,
)
from property.models import Property
from species.models import OwnedSpecies, Taxon

logger = logging.getLogger('sawps')


def string_to_boolean(string):
    """Convert a string to boolean.

    :param
    string: The string to convert
    :type
    string:str
    """
    if string in ['Yes', 'YES', 'yes']:
        return True
    return False


def string_to_number(string):
    """Convert a string to a number.

    :param
    string: The string to convert
    :type
    string:str
    """
    try:
        return float(string)
    except ValueError:
        return float(0)


@shared_task(name='upload_species_data')
def upload_species_data(upload_session_id):
    try:
        upload_session = UploadSpeciesCSV.objects.get(id=upload_session_id)
    except UploadSpeciesCSV.DoesNotExist:
        logger.error("upload session doesn't exist")
        return None

    encoding = 'utf-8-sig'
    row_num = 1

    with open(upload_session.process_file.path, encoding=encoding
              ) as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)

        for row in data:

            # get property
            try:
                property = Property.objects.get(
                    name=row["Property_name"],
                )
            except Property.DoesNotExist:
                upload_session.error_notes = 'Property does not exist'
                upload_session.canceled = True
                upload_session.save
                return None


            # Save Taxon
            taxon, taxon_created = Taxon.objects.get_or_create(
                scientific_name=row["Scientific_name"],
                common_name_varbatim=row["Common_name_verbatim"],
            )

            # Save OwnedSpecies
            owned_species, created = OwnedSpecies.objects.get_or_create(
                taxon=taxon,
                user=upload_session.uploader,
                property=property,
                area_available_to_species=float(row['Area_available__ha'])

            )

            # Save OpenCloseSystem
            open_sys, open_created = OpenCloseSystem.objects.get_or_create(
                name=row["Open/closed system"]
            )

            # save CountMethod
            count_meth, count_created = CountMethod.objects.get_or_create(
                name=row["CountMethod_verbatim"]
            )

            survey, created = SurveyMethod.objects.get_or_create(
                name=row["Survey_method_dropdown"]
            )

            # Save AnnualPopulation
            AnnualPopulation.objects.get_or_create(
                year=int(string_to_number(row['Count_Year'])),
                owned_species=owned_species,
                total=int(string_to_number(row['COUNT_TOTAL'])),
                adult_male=int(string_to_number(row['Count_adult_males'])),
                adult_female=int(string_to_number(row['Count_adult_females'])),
                juvenile_male=int(string_to_number(
                    row['Count_Juvenile_males'])),
                juvenile_female=int(string_to_number(
                    row['Count_Juvenile_females'])),
                sub_adult_total=int(string_to_number(
                    row['COUNT_subadult_TOTAL'])),
                sub_adult_male=int(string_to_number(
                    row['Count_subadult_male'])),
                sub_adult_female=int(string_to_number(
                    row['Count_subadult_female'])),
                juvenile_total=int(string_to_number(
                    row['COUNT_Juvenile_TOTAL'])),
                group=int(string_to_number(row['No_groups'])),
                open_close_system=open_sys,
                area_covered=float(string_to_number(
                    row['Area_available__ha'])),
                count_method=count_meth,
                survey_method=survey,
                presence=string_to_boolean(row["PresenceOnly"]),
                note=row["Notes"]

            )

            # Save AnnualPopulationPerActivity
            AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Planned translocation"),
                year=int(string_to_number(row['Count_Year'])),
                owned_species=owned_species,
                total=int(string_to_number(row['COUNT_TOTAL'])),
                note=row["Notes"],
                adult_male=int(string_to_number(
                    row["(Re)Introduction_adult_males"])),
                adult_female=int(string_to_number(
                    row["(Re)Introduction_adult_females"])),
                juvenile_male=int(string_to_number(
                    row["(Re)Introduction_male_juveniles"])),
                juvenile_female=int(string_to_number(
                    row["(Re)Introduction_female_juveniles"])),
                reintroduction_source=row["(Re)Introduction_source"],
                translocation_destination=row["Translocation_destination"],
                founder_population=string_to_boolean(row["FounderPop?"]),
            )

            upload_session.processed = True
            success_response = f'{row_num} row have been added to the database'
            upload_session.success_notes = (
                success_response
            )
            upload_session.save()
            row_num += 1
