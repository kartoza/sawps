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
    sampling_eff_nb = 0
    open_created_nb = 0
    survey_nb = 0
    pop_estim_nb = 0
    intake_nb = 0
    offtake_nb = 0
    hunt_nb = 0
    euthanasia_nb = 0
    unplanned_nb = 0
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
                upload_session.error_notes = "The property name: {} in the " \
                    "CSV line number {} does not match the selected " \
                    "property. Please replace it with {}.".format(
                        row["Property_name"], row_num, property_name)
                upload_session.save()
                continue

            # Get Taxon
            try:
                taxon = Taxon.objects.get(
                    scientific_name=row["Scientific_name"],
                    common_name_varbatim=row["Common_name_verbatim"],
                )
            except Taxon.DoesNotExist:
                upload_session.error_notes = \
                    "Taxon {} in row {} does not exist".format(
                        row["Scientific_name"], row_num
                    )
                upload_session.save()
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
                if c:
                    sampling_eff_nb += 1

            # Save OpenCloseSystem
            if row["open/close_system"]:
                open_sys, open_created = OpenCloseSystem.objects.get_or_create(
                    name=row["open/close_system"]
                )
                if open_created:
                    open_created_nb += 1

            # Save Survey method
            suv = row["If other (survey method), please explain"]
            if row["Survey_method"] or suv:
                survey, created = SurveyMethod.objects.get_or_create(
                    name=(row["Survey_method"] if row["Survey_method"] else
                          suv
                          )
                )
                if created:
                    survey_nb += 1

            # Save Population estimate category
            e = row["If other (population estimate category) , please explain"]
            if row["Population estimate category"] or e:
                p, pc = PopulationEstimateCategory.objects.get_or_create(name=(
                    row["Population estimate category"] if
                    row["Population estimate category"] else e

                ))
                if pc:
                    pop_estim_nb += 1

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
                if in_c:
                    intake_nb += 1

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
                if off_c:
                    offtake_nb += 1

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
                if hunt_c:
                    hunt_nb += 1

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
                if pe_c:
                    euthanasia_nb += 1

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
                if unp_c:
                    unplanned_nb += 1
            row_num += 1
            upload_session.processed = True
            upload_session.save()

    if upload_session.processed:
        if owned_species_created > 0 and annual_created_nb > 0:
            success_response = "{} rows have been uploaded. With {} Annual " \
                    "population, {} sampling effort coverage, {} " \
                    "open/close_system, {} survey method, {} population " \
                    "estimate category annual population " \
                    "per activity: {} Translocation (Intake)," \
                    "{} Translocation (Offtake), {} Planned Hunt/Cull" \
                    "{} Planned Euthanasia/DCA, {} Unplanned/Illegal " \
                    "Hunting".format(
                        owned_species_created,
                        annual_created_nb,
                        sampling_eff_nb,
                        open_created_nb,
                        survey_nb,
                        pop_estim_nb,
                        intake_nb,
                        offtake_nb,
                        hunt_nb,
                        euthanasia_nb,
                        unplanned_nb,
                    )
        else:
            success_response = "The {} rows have not been saved. " \
                "They already exist in the database.".format(annual_created_nb)

        upload_session.success_notes = (
            success_response
        )
        upload_session.save()
