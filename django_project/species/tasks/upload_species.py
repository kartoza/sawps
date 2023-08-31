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
    PopulationEstimateCategory,
    SamplingEffortCoverage,
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


def plural(number):
    if number > 1:
        return "rows have"
    return "row has"


@shared_task(name='upload_species_data')
def upload_species_data(upload_session_id):
    try:
        upload_session = UploadSpeciesCSV.objects.get(id=upload_session_id)
    except UploadSpeciesCSV.DoesNotExist:
        logger.error("upload session doesn't exist")
        return

    property_name = upload_session.property.name
    encoding = 'utf-8-sig'
    row_num = 1
    owned_species_created = 0
    annual_created_nb = 0
    taxa_error = []
    property_error = []
    line_added = 0

    with open(upload_session.process_file.path, encoding=encoding
              ) as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)

        for row in data:
            row_num += 1
            # get property
            try:
                property = Property.objects.get(
                    name=row["Property_name"],
                )
            except Property.DoesNotExist:
                property_error.append(
                    "{} in line number {}".format(
                        row["Property_name"], row_num
                    )
                )
                continue

            # Get Taxon
            try:
                taxon = Taxon.objects.get(
                    scientific_name=row["Scientific_name"],
                    common_name_varbatim=row["Common_name_verbatim"],
                )
            except Taxon.DoesNotExist:
                taxa_error.append("{} in line number {}".format(
                    row["Scientific_name"], row_num
                ))
                continue

            # Save OwnedSpecies
            owned_species, cr = OwnedSpecies.objects.get_or_create(
                taxon=taxon,
                user=upload_session.uploader,
                property=property,
                area_available_to_species=float(row[
                    "Area_available to population (total enclosure area)_ha"])
            )
            if cr:
                owned_species_created += 1

            # Save Sampling Effort Coverage
            if row["Sampling_effort_coverage"]:
                sampling_eff, c = SamplingEffortCoverage.objects.get_or_create(
                    name=row["Sampling_effort_coverage"]
                )

            # Save OpenCloseSystem
            if row["open/close_system"]:
                open_sys, open_created = OpenCloseSystem.objects.get_or_create(
                    name=row["open/close_system"]
                )

            # Save Survey method
            suv = row["If other (survey method), please explain"]
            if row["Survey_method"] or suv:
                survey, created = SurveyMethod.objects.get_or_create(
                    name=(row["Survey_method"] if row["Survey_method"] else
                          suv
                          )
                )

            # Save Population estimate category
            e = row["If other (population estimate category) , please explain"]
            if row["Population estimate category"] or e:
                p, pc = PopulationEstimateCategory.objects.get_or_create(name=(
                    row["Population estimate category"] if
                    row["Population estimate category"] else e

                ))

            # Save AnnualPopulation
            annual, annual_created = AnnualPopulation.objects.get_or_create(
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
                survey_method=survey,
                presence=string_to_boolean(row["presence/absence"]),
                upper_confidence_level=float(string_to_number(
                    row["Upper confidence limits for population estimate"])),
                lower_confidence_level=float(string_to_number(
                    row["Lower confidence limits for population estimate"])),
                certainty_of_bounds=int(string_to_number(
                    row["Certainity of population bounds"])),
                sampling_effort_coverage=sampling_eff,
                population_estimate_certainty=int(string_to_number(
                    row["Population estimate certainty"])),
                population_estimate_category=p
            )
            if annual_created:
                annual_created_nb += 1

            # Save AnnualPopulationPerActivity translocation intake
            if row["(Re)Introduction_TOTAL"]:
                take, in_c = AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Translocation (Intake)"),
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
                        row["Permit_number (if applicable)"]))
                )

            # Save AnnualPopulationPerActivity translocation offtake
            if row["Translocation_offtake_total"]:
                off, off_c = AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Translocation (Offtake)"),
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
                h, hunt_c = AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned Hunt/Cull"),
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
                pe, pe_c = AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Planned Euthanasia/DCA"),
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
                unp, unp_c = AnnualPopulationPerActivity.objects.get_or_create(
                    activity_type=ActivityType.objects.get(
                        name="Unplanned/Illegal Hunting"),
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
                        "Unplanned/illegal hunting_Offtake_female_juveniles"]))
                )
            line_added += 1
            upload_session.processed = True
            upload_session.save()

    if len(taxa_error) > 0 or len(property_error) > 0:
        taxa_message = ''
        property_message = ''
        for error in taxa_error:
            taxa_message += error + ','
        if len(taxa_error) > 0:
            v = 'do not exist.' if len(taxa_error) > 1 \
                else 'does not exist'
            taxa_message += v + ' in the database. ' \
                'Please select species available in the dropdown only.'
            taxa_message = "Taxon name: " + taxa_message

        for error in property_error:
            property_message += error + ','
        if len(property_error) > 0:
            v = 'do' if len(property_error) > 1 else 'does'
            property_message += v + " not match the selected property. " \
                "Please replace it with {}.".format(property_name)
            property_message = "The property name: " + property_message
        upload_session.error_notes =  \
            property_message + '\n' + taxa_message

    if upload_session.processed:
        if owned_species_created > 0 and annual_created_nb > 0:
            success_response = "{} {} been uploaded.".format(
                        line_added, plural(line_added)
                    )
            if owned_species_created < line_added:
                success_response = "{} {} been uploaded.The {} " \
                    "{} not been saved. " \
                    "They already exist in the database.".format(
                        owned_species_created,
                        plural(owned_species_created),
                        plural(line_added - owned_species_created),
                        line_added - owned_species_created
                    )
        else:
            success_response = "The {} {} not been saved. " \
                "They already exist in the database.".format(
                    line_added, plural(line_added))

        upload_session.success_notes = (
            success_response
        )
    upload_session.save()
