import logging
import csv
import re
import copy
import tempfile
import pandas as pd
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError
from frontend.models.upload import UploadSpeciesCSV
from activity.models import ActivityType
from occurrence.models import SurveyMethod
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    OpenCloseSystem,
    PopulationEstimateCategory,
    SamplingEffortCoverage,
)
from property.models import Property
from species.models import Taxon

from species.scripts.upload_file_scripts import *  # noqa
from frontend.utils.statistical_model import (
    mark_model_output_as_outdated_by_species_list
)
from stakeholder.models import (
    OrganisationRepresentative,
    OrganisationUser
)

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


class SpeciesCSVUpload(object):
    upload_session = UploadSpeciesCSV.objects.none()
    error_list = []
    created_list = 0
    existed_list = 0
    headers = []
    total_rows = 0
    row_error = []
    csv_dict_reader = None
    species_id_list = []

    def process_started(self):
        pass

    def process_ended(self):
        pass

    def start(self, encoding='ISO-8859-1'):
        """
        Start processing the csv file from upload session
        """
        self.error_list = []
        self.species_id_list = []
        uploaded_file = self.upload_session.process_file
        if self.upload_session.process_file.path.endswith('.xlsx'):
            excel = pd.ExcelFile(self.upload_session.process_file)
            dataframe = excel.parse(SHEET_TITLE)
            with tempfile.NamedTemporaryFile(mode='w', delete=False) \
                    as csv_file:
                dataframe.to_csv(csv_file.name, index=False)
                uploaded_file = csv_file
        try:
            read_line = uploaded_file.readlines()
            uploaded_file_path = uploaded_file.path
        except ValueError:
            file = open(uploaded_file.name)
            read_line = file.readlines()
            uploaded_file_path = uploaded_file.name
        self.total_rows = len(
            read_line
        ) - 1
        self.process_started()
        processed = False

        with open(
                uploaded_file_path,
                encoding=encoding) as csv_file:
            try:
                self.csv_dict_reader = csv.DictReader(csv_file)
                self.process_csv_dict_reader()
                processed = True
            except UnicodeDecodeError:
                pass
        if not processed:
            with open(
                    uploaded_file_path,
                    encoding=encoding
            ) as csv_file:
                try:
                    self.csv_dict_reader = csv.DictReader(csv_file)
                    self.process_csv_dict_reader()
                    processed = True
                except UnicodeDecodeError:
                    pass
        if not processed:
            self.upload_session.canceled = True
            self.upload_session.save()
            self.process_ended()
            return
        self.process_ended()

    def error_row(self, message):
        """
        Get error in row
        :param message: error message for a row
        """
        self.row_error.append(message)

    def error_file(self, row):
        """
        Write to error file
        :param row: error data
        """
        if len(self.row_error) > 0:
            logger.log(
                level=logging.ERROR,
                msg=' '.join(self.row_error)
            )
            row['error_message'] = ' '.join(self.row_error)
            self.error_list.append(row)

    def finish(self, headers):
        """
        Finishing the csv upload process
        """
        file_name = (
            self.upload_session.process_file.name.replace(
                'species/', '')
        )
        file_path = (
            self.upload_session.process_file.path.replace(file_name, '')
        )

        # Create error file
        # TODO : Done it simultaneously with file processing
        if self.error_list:
            error_headers = copy.deepcopy(headers)
            if 'error_message' not in error_headers:
                error_headers.insert(0, 'error_message')
            error_file_path = '{path}error_{name}'.format(
                path=file_path,
                name=file_name
            )

            excel_error = None

            if error_file_path.endswith('.xlsx'):
                excel_error = error_file_path
                logger.log(
                    level=logging.ERROR,
                    msg=str(excel_error)
                )
                with tempfile.NamedTemporaryFile(mode='w', delete=False)\
                        as csv_file:
                    error_file_path = csv_file.name

            with open(error_file_path, mode='w') as csv_file:
                writer = csv.writer(
                    csv_file, delimiter=',', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(error_headers)
                for data in self.error_list:
                    data_list = []
                    for key in error_headers:
                        try:
                            data_list.append(data[key])
                        except KeyError:
                            continue
                    writer.writerow(data_list)

            if excel_error:
                with pd.ExcelWriter(excel_error, engine='openpyxl', mode='w')\
                        as writer:
                    dataframe = pd.read_csv(error_file_path)
                    dataframe.to_excel(
                        writer,
                        sheet_name=SHEET_TITLE,
                        index=False
                    )

            self.upload_session.error_file.name = (
                'species/error_{}'.format(
                    file_name
                )
            )

        # Create success message
        success_message = None
        if self.created_list > 0 and self.existed_list == 0:
            success_message = "{} rows uploaded successfully." \
                              "".format(self.created_list)

        if self.existed_list > 0 and self.created_list == 0:
            success_message = "{} rows already exist and have been " \
                              "overwritten." \
                              "".format(self.existed_list)

        if self.existed_list > 0 and self.created_list > 0:
            success_message = "{} rows already exist and have been " \
                              "overwritten. {} " \
                              "rows uploaded successfully." \
                              "".format(self.existed_list, self.created_list)

        if success_message:
            self.upload_session.success_notes = success_message

        if self.total_rows == 0:
            self.upload_session.error_notes = (
                'You have uploaded empty spreadsheet, please check again.'
            )

        self.upload_session.processed = True
        self.upload_session.progress = 'Finished'
        self.upload_session.save()
        if self.created_list > 0 or self.existed_list > 0:
            mark_model_output_as_outdated_by_species_list(self.species_id_list)

    def row_value(self, row, key):
        """
        Get row value by key
        :param row: row data
        :param key: key
        :return: row value
        """
        row_value = ''
        try:
            row_value = row[key]
            row_value = row_value.replace('\xa0', ' ')
            row_value = row_value.replace('\xc2', '')
            row_value = row_value.replace('\\xa0', '')
            row_value = row_value.strip()
            row_value = re.sub(' +', ' ', row_value)
        except KeyError:
            pass
        return row_value

    def process_csv_dict_reader(self):
        """
        Read and process data from csv file
        """
        index = 1
        self.created_list = 0
        self.existed_list = 0
        for row in self.csv_dict_reader:
            self.row_error = []
            if UploadSpeciesCSV.objects.get(
                    id=self.upload_session.id).canceled:
                return
            logger.debug(row)
            self.upload_session.progress = '{index}/{total}'.format(
                index=index,
                total=self.total_rows
            )
            self.upload_session.save()
            index += 1
            self.process_data(row=row)
            self.error_file(row)
        self.finish(self.csv_dict_reader.fieldnames)

    def get_property(self, property_code):
        property_selected = self.upload_session.property.short_code
        if property_code == property_selected:
            try:
                property = Property.objects.get(
                        short_code=property_selected,
                )
            except Property.DoesNotExist:
                return
            except Property.MultipleObjectsReturned:
                return

            return property

    def get_taxon(self, common_name, scientific_name):
        if common_name or scientific_name:
            try:
                taxon = Taxon.objects.get(
                    scientific_name__iexact=scientific_name,
                    common_name_verbatim__iexact=common_name
                )
            except Taxon.DoesNotExist:
                return
            return taxon

    def sampling_effort(self, row):
        sampling_effort = self.row_value(row, SAMPLING_EFFORT)
        if sampling_effort:
            sampling_eff, c = SamplingEffortCoverage.objects.get_or_create(
                name__iexact=sampling_effort,
                defaults={
                    'name': sampling_effort
                }
            )
            return sampling_eff
        return None

    def open_close_system(self, row):
        open_close_sys = self.row_value(row, OPEN_SYS)
        if open_close_sys:
            try:
                open_sys = OpenCloseSystem.objects.get(
                    name__iexact=open_close_sys
                )
            except OpenCloseSystem.DoesNotExist:
                self.error_row(
                    f"Open/Close system '{open_close_sys}' does not exist"
                )
                return None
            return open_sys
        return None

    # Save Survey method
    def survey_method(self, survey):
        """Get survey method."""
        if not survey:
            return None

        else:
            survey, created = SurveyMethod.objects.get_or_create(
                name__iexact=survey,
                defaults={
                    'name': survey
                }
            )
            return survey

    def population_estimate_category(self, pop_est):
        """ Save Population estimate category.
        """
        if not pop_est:
            return None
        else:
            p, pc = PopulationEstimateCategory.objects.get_or_create(
                    name__iexact=pop_est,
                    defaults={
                        'name': pop_est
                    }
            )
            return p

    def check_compulsory_fields(self, row):
        """Check if compulsory fields are empty."""

        for field in COMPULSORY_FIELDS:
            if not self.row_value(row, field):
                self.error_row(
                    message="The value of the compulsory field {} "
                            "is empty.".format(field)
                )

    def save_population_per_activity(
            self, row, activity, year, annual_population, total, total_males,
            total_females, male_juv, female_juv
    ):

        pop = None
        try:
            pop, in_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name__iexact=activity),
                year=int(string_to_number(year)),
                annual_population=annual_population,
                total=int(string_to_number(
                    self.row_value(row, total))),
                adult_male=int(string_to_number(
                    self.row_value(row, total_males))),
                adult_female=int(string_to_number(
                    self.row_value(row, total_females))),
                juvenile_male=int(string_to_number(
                    self.row_value(row, male_juv))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, female_juv))),
            )
        except IntegrityError:
            self.error_row(
                message="The total of {} and {} must not exceed {}.".format(
                    total_males,
                    total_females,
                    total)
            )
        return pop

    def check_if_not_superuser(self):
        if self.upload_session.uploader is None:
            return True
        return not self.upload_session.uploader.is_superuser

    def process_data(self, row):
        """Processing row of csv file."""

        # check compulsory fields
        self.check_compulsory_fields(row)
        property = taxon = None
        property_code = self.row_value(row, PROPERTY)
        if property_code:
            property = self.get_property(property_code)

            if not property:
                self.error_row(
                    message="Property code {} doesn't match the selected "
                            "property. Please replace it with {}.".format(
                                self.row_value(row, PROPERTY),
                                self.upload_session.property.short_code)
                )

        scientific_name = self.row_value(row, SCIENTIFIC_NAME)
        common_name = self.row_value(row, COMMON_NAME)
        if scientific_name and common_name:
            taxon = self.get_taxon(common_name, scientific_name)
            if not taxon:
                self.error_row(
                    message="{} doesn't exist in the "
                            "database. Please select species available "
                            "in the dropdown only.".format(
                                self.row_value(row, SCIENTIFIC_NAME)
                            )
                )
            elif taxon.id not in self.species_id_list:
                self.species_id_list.append(taxon.id)

        area_available_to_species = self.row_value(row, AREA)
        # validate area_available_to_species must be greater than 0 and
        # less than property size
        area_available_to_species_num = int(
            string_to_number(area_available_to_species))
        if (
            area_available_to_species_num <= 0 or
            area_available_to_species_num >
            self.upload_session.property.property_size_ha
        ):
            self.error_row(
                message="Area available to species must be greater than 0 "
                        "and less than or equal to property area size "
                        "({:.2f} ha).".format(
                            self.upload_session.property.property_size_ha
                        )
            )

        survey = self.row_value(row, SURVEY_METHOD)
        survey_method = self.survey_method(survey)
        survey_other = self.row_value(row, IF_OTHER_SURVEY)
        sur_other = None
        if survey_method and survey_method.name == IF_OTHER_SURVEY_VAL:
            if not survey_other:
                self.error_row(
                    message="The value of field {} "
                            "is empty.".format(IF_OTHER_SURVEY)
                )
            sur_other = survey_other

        open_close_system = self.open_close_system(row)
        pop_est = self.row_value(row, POPULATION_ESTIMATE_CATEGORY)
        population_estimate = self.population_estimate_category(pop_est)
        population_other = self.row_value(row, IF_OTHER_POPULATION)
        pop_other = None
        if population_estimate and \
                population_estimate.name == IF_OTHER_POPULATION_VAL:
            if not population_other:
                self.error_row(
                    message="The value of field {} "
                            "is empty.".format(IF_OTHER_POPULATION)
                )
                # return
            pop_other = population_other

        year = self.row_value(row, YEAR)
        if year.isdigit():
            if int(year) > timezone.now().year:
                self.error_row(
                    message=f"'{YEAR}' with value {year} exceeds current year."
                )
        count_total = self.row_value(row, COUNT_TOTAL)
        presence = self.row_value(row, PRESENCE)
        pop_certainty = self.row_value(row, POPULATION_ESTIMATE_CERTAINTY)

        if property and taxon and self.check_if_not_superuser():
            is_organisation_manager = (
                OrganisationRepresentative.objects.filter(
                    organisation=property.organisation,
                    user=self.upload_session.uploader
                )
            )
            existing_data = AnnualPopulation.objects.filter(
                year=int(string_to_number(year)),
                taxon=taxon,
                property=property
            ).first()
            if existing_data:
                # validate if user can update the data: uploader or manager
                if (
                    not existing_data.is_editable(
                        self.upload_session.uploader)
                ):
                    self.error_row(
                        message="You are not allowed to update data of "
                                "property {} and species {} in year {}".format(
                                    property_code, scientific_name, year
                                )
                    )
            else:
                # validate if user can add data to the property
                is_organisation_member = OrganisationUser.objects.filter(
                    organisation=property.organisation,
                    user=self.upload_session.uploader
                )
                if not is_organisation_manager and not is_organisation_member:
                    self.error_row(
                        message="You are not allowed to add data to "
                                "property {}".format(property_code)
                    )

        if len(self.row_error) > 0:
            return

        # Save AnnualPopulation
        try:
            annual, annual_created = AnnualPopulation.objects.update_or_create(
                year=int(string_to_number(year)),
                taxon=taxon,
                property=property,
                defaults={
                    'user': self.upload_session.uploader,
                    'area_available_to_species': area_available_to_species,
                    'total': int(string_to_number(count_total)),
                    'adult_total': int(string_to_number(
                        self.row_value(row, COUNT_ADULT_TOTAL))),
                    'adult_male': int(string_to_number(
                        self.row_value(row, COUNT_ADULT_MALES))),
                    'adult_female': int(string_to_number(
                        self.row_value(row, COUNT_ADULT_FEMALES))),
                    'juvenile_male': int(string_to_number(
                        self.row_value(row, COUNT_JUVENILE_MALES))),
                    'juvenile_female': int(string_to_number(
                        self.row_value(row, COUNT_JUVENILE_FEMALES))),
                    'sub_adult_total': int(string_to_number(
                        self.row_value(row, COUNT_SUBADULT_TOTAL))),
                    'sub_adult_male': int(string_to_number(
                        self.row_value(row, COUNT_SUBADULT_MALE))),
                    'sub_adult_female': int(string_to_number(
                        self.row_value(row, COUNT_SUBADULT_FEMALE))),
                    'juvenile_total': int(string_to_number(
                        self.row_value(row, COUNT_JUVENILE_TOTAL))),
                    'group': int(string_to_number(self.row_value(row, GROUP))),
                    'open_close_system': open_close_system,
                    'survey_method': survey_method,
                    'presence': string_to_boolean(presence),
                    'upper_confidence_level': float(string_to_number(
                        self.row_value(row, UPPER))),
                    'lower_confidence_level': float(string_to_number(
                        self.row_value(row, LOWER))),
                    'certainty_of_bounds': int(string_to_number(
                        self.row_value(row, CERTAINTY_OF_POPULATION))),
                    'sampling_effort_coverage': self.sampling_effort(row),
                    'population_estimate_certainty': int(
                        string_to_number(pop_certainty)),
                    'population_estimate_category': population_estimate,
                    'survey_method_other': sur_other,
                    'population_estimate_category_other': pop_other
                }
            )
            annual.clean()
        except (IntegrityError, ValidationError):
            if annual.pk:
                annual.delete()
            self.error_row(
                message="The total of {} and {} must not exceed {}.".format(
                        COUNT_ADULT_MALES,
                        COUNT_ADULT_FEMALES,
                        COUNT_TOTAL)
            )
            logger.log(
                level=logging.ERROR,
                msg=str(self.row_error)
            )
            return

        if annual_created:
            self.created_list += 1
        else:
            self.existed_list += 1
            # if updated, cleared population per activity
            AnnualPopulationPerActivity.objects.filter(
                annual_population=annual
            ).delete()

        # Save AnnualPopulationPerActivity translocation intake
        if self.row_value(row, INTRODUCTION_TOTAL):
            intake = self.save_population_per_activity(
                row, "Translocation (Intake)", year,
                annual, INTRODUCTION_TOTAL,
                INTRODUCTION_TOTAL_MALES, INTRODUCTION_TOTAL_FEMALES,
                INTRODUCTION_MALE_JUV, INTRODUCTION_FEMALE_JUV
            )
            intake_data = {
                "reintroduction_source": self.row_value(row,
                                                        INTRODUCTION_SOURCE),
                "founder_population": string_to_boolean(
                    self.row_value(row, FOUNDER_POPULATION)
                ),
                "intake_permit": self.row_value(
                    row, INTRODUCTION_PERMIT_NUMBER
                )
            }
            if intake:
                intake = AnnualPopulationPerActivity.objects.filter(
                    id=intake.id
                )
                intake.update(**intake_data)

        # Save AnnualPopulationPerActivity translocation offtake
        if self.row_value(row, TRANS_OFFTAKE_TOTAL):
            off_take = self.save_population_per_activity(
                row, "Translocation (Offtake)", year,
                annual, TRANS_OFFTAKE_TOTAL,
                TRANS_OFFTAKE_ADULTE_MALES, TRANS_OFFTAKE_ADULTE_FEMALES,
                TRANS_OFFTAKE_MALE_JUV, TRANS_OFFTAKE_FEMALE_JUV
            )
            off_take_data = {
                "translocation_destination": self.row_value(
                    row, TRANS_DESTINATION),
                "offtake_permit": self.row_value(
                    row, TRANS_OFFTAKE_PERMIT_NUMBER)
            }
            if off_take:
                off_take = AnnualPopulationPerActivity.objects.filter(
                    id=off_take.id
                )
                off_take.update(**off_take_data)

        # Save AnnualPopulationPerActivity Planned hunt/cull
        if self.row_value(row, PLANNED_HUNT_TOTAL):
            hunt = self.save_population_per_activity(
                row, "Planned Hunt/Cull", year,
                annual, PLANNED_HUNT_TOTAL,
                PLANNED_HUNT_OFFTAKE_ADULT_MALES,
                PLANNED_HUNT_OFFTAKE_ADULT_FAMALES,
                PLANNED_HUNT_OFFTAKE_MALE_JUV,
                PLANNED_HUNT_OFFTAKE_FEMALE_JUV
            )
            hunt_data = {
                "offtake_permit": self.row_value(
                    row, PLANNED_HUNT_PERMIT_NUMBER
                )

            }
            if hunt:
                hunt = AnnualPopulationPerActivity.objects.filter(
                    id=hunt.id
                )
                hunt.update(**hunt_data)

        # Save AnnualPopulationPerActivity Planned euthanasia
        if self.row_value(row, PLANNED_EUTH_TOTAL):
            planned = self.save_population_per_activity(
                row, "Planned Euthanasia/DCA", year,
                annual, PLANNED_EUTH_TOTAL,
                PLANNED_EUTH_OFFTAKE_ADULT_MALES,
                PLANNED_EUTH_OFFTAKE_ADULT_FAMALES,
                PLANNED_EUTH_OFFTAKE_MALE_JUV,
                PLANNED_EUTH_OFFTAKE_FEMALE_JUV
            )
            planned_data = {
                "offtake_permit": self.row_value(
                    row, PLANNED_EUTH_PERMIT_NUMBER
                )

            }
            if planned:
                planned = AnnualPopulationPerActivity.objects.filter(
                    id=planned.id
                )
                planned.update(**planned_data)

        # Save AnnualPopulationPerActivity Unplanned/illegal hunting
        if self.row_value(row, UNPLANNED_HUNT_TOTAL):
            hunting = self.save_population_per_activity(
                row, "Unplanned/Illegal Hunting", year,
                annual, UNPLANNED_HUNT_TOTAL,
                UNPLANNED_HUNT_OFFTAKE_ADULT_MALES,
                UNPLANNED_HUNT_OFFTAKE_ADULT_FAMALES,
                UNPLANNED_HUNT_OFFTAKE_MALE_JUV,
                PLANNED_EUTH_OFFTAKE_FEMALE_JUV
            )
            hunting_data = {
                "offtake_permit": self.row_value(
                    row, UNPLANNED_HUNT_OFFTAKE_FEMALE_JUV
                )

            }
            if hunting:
                hunting = AnnualPopulationPerActivity.objects.filter(
                    id=hunting.id
                )
                hunting.update(**hunting_data)
