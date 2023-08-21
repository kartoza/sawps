import csv
import logging

from activity.models import ActivityType
from celery import shared_task
from frontend.models import UploadSpeciesCSV
from occurrence.models import SurveyMethod
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
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
    success_response = None
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
                return

            # Get Taxon
            try:
                taxon = Taxon.objects.get(
                    scientific_name=row["Scientific_name"],
                    common_name_varbatim=row["Common_name_verbatim"],
                )
            except Taxon.DoesNotExist:
                upload_session.error_notes = 'Taxon does not exist'
                upload_session.canceled = True
                upload_session.save
                return

            # Save OwnedSpecies
            owned_species, created = OwnedSpecies.objects.get_or_create(
                taxon=taxon,
                user=upload_session.uploader,
                property=property,
                area_available_to_species=float(
                    row
                    ["Area_available to population (total enclosure area)_ha"]
                )

            )

            # Save OpenCloseSystem
            open_sys, open_created = OpenCloseSystem.objects.get_or_create(
                name=row["open/close_system"]
            )

            survey, created = SurveyMethod.objects.get_or_create(
                name=row["Survey_method"]
            )

            # Save AnnualPopulation
            AnnualPopulation.objects.get_or_create(
                year=int(string_to_number(row["Year of estimate"])),
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
                group=int(string_to_number(
                    row["No. subpopulations / groups"])),
                open_close_system=open_sys,
                area_covered=float(string_to_number(
                    row['Area_available__ha'])),
                survey_method=survey,
                presence=string_to_boolean(row["presence/absence"]),

            )

            # Save AnnualPopulationPerActivity Planned translocation intake
            if row["(Re)Introduction_TOTAL"]:
                AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned translocation"),
                    year=int(string_to_number(row['Year of estimate'])),
                    owned_species=owned_species,
                    total=int(string_to_number(row["(Re)Introduction_TOTAL"])),
                    # note=row["Notes"],
                    adult_male=int(string_to_number(
                        row["(Re)Introduction_adult_males"])),
                    adult_female=int(string_to_number(
                        row["(Re)Introduction_adult_females"])),
                    juvenile_male=int(string_to_number(
                        row["(Re)Introduction_male_juveniles"])),
                    juvenile_female=int(string_to_number(
                        row["(Re)Introduction_female_juveniles"])),
                    reintroduction_source=row["(Re)Introduction_source"],
                    founder_population=string_to_boolean(
                        row["Founder population?"]),
                    intake_permit=int(string_to_number(
                        row["Permit_number (if applicable)?"]))
                )

            # Save AnnualPopulationPerActivity Planned translocation offtake
            if row["Translocation_offtake_total"]:
                AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned translocation"),
                    year=int(string_to_number(row['Year of estimate'])),
                    owned_species=owned_species,
                    total=int(string_to_number(
                        row["Translocation_offtake_total"])),
                    # note=row["Notes"],
                    adult_male=int(string_to_number(
                        row["Translocation_Offtake_adult_males"])),
                    adult_female=int(string_to_number(
                        row["Translocation_Offtake_adult_females"])),
                    juvenile_male=int(string_to_number(
                        row["Translocation_Offtake_male_juveniles"])),
                    juvenile_female=int(string_to_number(
                        row["Translocation_Offtake_female_juveniles"])),
                    translocation_destination=row["Translocation_destination"],
                    offtake_permit=int(string_to_number(
                        row["Translocation_Offtake_Permit_number"]))
                )

            # Save AnnualPopulationPerActivity Planned hunt/cull
            if row["Planned hunt/culling_TOTAL"]:
                AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned hunt/cull"),
                    year=int(string_to_number(row['Year of estimate'])),
                    owned_species=owned_species,
                    total=int(string_to_number(
                        row["Planned hunt/culling_TOTAL"])),
                    # note=row["Notes"],
                    adult_male=int(string_to_number(
                        row["Planned hunt/culling_Offtake_adult_males"])),
                    adult_female=int(string_to_number(
                        row["Planned hunt/culling_Offtake_adult_females"])),
                    juvenile_male=int(string_to_number(
                        row["Planned hunt/culling_Offtake_male_juveniles"])),
                    juvenile_female=int(string_to_number(
                        row["Planned hunt/culling_Offtake_female_juveniles"])),
                    offtake_permit=int(string_to_number(
                        row["Planned hunt/culling_Permit_number"]))
                )

            # Save AnnualPopulationPerActivity Planned euthanasia
            if row["Planned euthanasia_TOTAL"]:
                AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned euthanasia"),
                    year=int(string_to_number(row['Year of estimate'])),
                    owned_species=owned_species,
                    total=int(string_to_number(
                        row["Planned euthanasia_TOTAL"])),
                    # note=row["Notes"],
                    adult_male=int(string_to_number(
                        row["Planned euthanasia_Offtake_adult_males"])),
                    adult_female=int(string_to_number(
                        row["Planned euthanasia_Offtake_adult_females"])),
                    juvenile_male=int(string_to_number(
                        row["Planned euthanasia_Offtake_male_juveniles"])),
                    juvenile_female=int(string_to_number(
                        row["Planned euthanasia_Offtake_female_juveniles"])),
                    offtake_permit=int(string_to_number(
                        row["Planned euthanasia_Permit_number"]))
                )

            # Save AnnualPopulationPerActivity Unplanned/illegal hunting
            if row["Unplanned/illegal hunting_TOTAL"]:
                AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Unplanned/illegal hunting"),
                    year=int(string_to_number(row['Year of estimate'])),
                    owned_species=owned_species,
                    total=int(string_to_number(
                        row["Unplanned/illegal hunting_TOTAL"])),
                    # note=row["Notes"],
                    adult_male=int(string_to_number(
                        row["Unplanned/illegal hunting_Offtake_adult_males"]
                    )),
                    adult_female=int(string_to_number(
                        row[
                            "Unplanned/illegal hunting_Offtake_adult_females"
                        ])),
                    juvenile_male=int(string_to_number(
                        row["Unplanned/illegal hunting_Offtake_male_juveniles"]
                    )),
                    juvenile_female=int(string_to_number(row[
                        "Unplanned/illegal hunting_Offtake_female_juveniles"
                    ]))
                )

            upload_session.processed = True
            success_response = row_num
            upload_session.success_notes = (
                success_response
            )
            upload_session.save()
            row_num += 1
