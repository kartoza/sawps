import logging
import csv
import re
import copy
import tempfile
import pandas as pd
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
from species.models import OwnedSpecies, Taxon

from species.scripts.upload_file_scripts import *  # noqa

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
    csv_dict_reader = None

    def process_started(self):
        pass

    def process_ended(self):
        pass

    def start(self, encoding='ISO-8859-1'):
        """
        Start processing the csv file from upload session
        """
        self.error_list = []
        self.success_list = []
        self.property = self.upload_session.property
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

    def error_file(self, row, message):
        """
        Write to error file
        :param row: error data
        :param message: error message for this row
        """
        logger.log(
            level=logging.ERROR,
            msg=str(message)
        )
        row['error_message'] = message
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
            success_message = "{} rows uploaded successfully."

        if self.existed_list > 0 and self.created_list == 0:
            success_message = "{} rows already exist in the database."

        if self.existed_list > 0 or self.created_list > 0:
            success_message = "{} rows already exist in the database. {} " \
                              "uploaded successfully.".\
                format(self.existed_list, self.created_list)

        if success_message:
            self.upload_session.success_notes = success_message

        self.upload_session.processed = True
        self.upload_session.progress = 'Finished'
        self.upload_session.save()

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
        for row in self.csv_dict_reader:
            if UploadSpeciesCSV.objects.get(
                    id=self.upload_session.id).canceled:
                print('Canceled')
                return
            logger.debug(row)
            self.upload_session.progress = '{index}/{total}'.format(
                index=index,
                total=self.total_rows
            )
            self.upload_session.save()
            index += 1
            self.process_data(row=row)

        self.finish(self.csv_dict_reader.fieldnames)

    def get_property(self, property_name):
        if property_name:
            try:
                property = Property.objects.get(
                        name=property_name,
                )
            except Property.DoesNotExist:
                return

            return property

    def get_taxon(self, common_name, scientific_name):
        if common_name or scientific_name:
            try:
                taxon = Taxon.objects.get(
                    scientific_name=scientific_name,
                    common_name_varbatim=common_name
                )
            except Taxon.DoesNotExist:
                return None
            return taxon

    def sampling_effort(self, row):
        sampling_effort = self.row_value(row, SAMPLING_EFFORT)
        if sampling_effort:
            sampling_eff, c = SamplingEffortCoverage.objects.get_or_create(
                name=sampling_effort
            )
            return sampling_eff
        return None

    def open_close_system(self, row):
        open_close_sys = self.row_value(row, OPEN_SYS)
        if open_close_sys:
            open_sys, open_created = OpenCloseSystem.objects.get_or_create(
                name=open_close_sys
            )
            return open_sys
        return None

    # Save Survey method
    def survey_method(self, survey):
        """Get survey method."""
        if not survey:
            return None

        else:
            survey, created = SurveyMethod.objects.get_or_create(
                name=survey
            )
            return survey

    def population_estimate_category(self, pop_est):
        """ Save Population estimate category.
        """
        if not pop_est:
            return None
        else:
            p, pc = PopulationEstimateCategory.objects.get_or_create(
                    name=pop_est)
            return p

    def check_compulsory_fields(self, row):
        """Check if compulsory fields are empty."""

        for field in COMPULSORY_FIELDS:
            if not self.row_value(row, field):
                self.error_file(
                    row=row,
                    message="The value of the compulsory field {} "
                            "is empty.".format(field)
                )
                return

    def process_data(self, row):
        """Processing row of csv file."""

        # check compulsory fields
        self.check_compulsory_fields(row)

        property_name = self.row_value(row, PROPERTY)
        if not property_name:
            return
        property = self.get_property(property_name)

        if not property:
            self.error_file(
                row=row,
                message="Property name {} doesn't match the selected "
                        "property. Please replace it with {}".format(
                            self.row_value(row, PROPERTY),
                            self.upload_session.property.name)
            )
            return

        scientific_name = self.row_value(row, SCIENTIFIC_NAME)
        common_name = self.row_value(row, COMMON_NAME)

        if not scientific_name or not common_name:
            return

        taxon = self.get_taxon(common_name, scientific_name)
        if not taxon:
            self.error_file(
                row=row,
                message="{} doesn't exist in the "
                        "database. Please select species available "
                        "in the dropdown only.".format(
                            self.row_value(row, SCIENTIFIC_NAME)
                        )
            )
            return

        area_available_to_species = self.row_value(row, AREA)
        if not area_available_to_species:
            return

        owned_species, cr = OwnedSpecies.objects.get_or_create(
            taxon=taxon,
            user=self.upload_session.uploader,
            property=property,
            area_available_to_species=area_available_to_species
        )

        survey = self.row_value(row, SURVEY_METHOD)
        survey_method = self.survey_method(survey)
        survey_other = self.row_value(row, IF_OTHER_SURVEY)
        sur_other = None
        if survey_method.name == IF_OTHER_SURVEY_VAL:
            if not survey_other:
                self.error_file(
                    row=row,
                    message="The value of field {} "
                            "is empty.".format(IF_OTHER_SURVEY)
                )
                return
            sur_other = survey_other

        open_close_system = self.open_close_system(row)
        if not open_close_system:
            return

        pop_est = self.row_value(row, POPULATION_ESTIMATE_CATEGORY)
        if not pop_est:
            return
        population_estimate = self.population_estimate_category(pop_est)
        population_other = self.row_value(row, IF_OTHER_POPULATION)
        pop_other = None
        if population_estimate.name == IF_OTHER_POPULATION_VAL:
            if not population_other:
                self.error_file(
                    row=row,
                    message="The value of field {} "
                            "is empty.".format(IF_OTHER_POPULATION)
                )
                return
            pop_other = population_other

        year = self.row_value(row, YEAR)
        if not year:
            return

        count_total = self.row_value(row, COUNT_TOTAL)
        if not count_total:
            return

        presence = self.row_value(row, PRESENCE)
        if not presence:
            return

        pop_certainty = self.row_value(row, POPULATION_ESTIMATE_CERTAINTY)
        if not pop_certainty:
            return

        # Save AnnualPopulation
        annual, annual_created = AnnualPopulation.objects.get_or_create(
            year=int(string_to_number(year)),
            owned_species=owned_species,
            total=int(string_to_number(count_total)),
            adult_male=int(string_to_number(
                self.row_value(row, COUNT_ADULT_MALES))),
            adult_female=int(string_to_number(
                self.row_value(row, COUNT_ADULT_FEMALES))),
            juvenile_male=int(string_to_number(
                self.row_value(row, COUNT_JUVENILE_MALES))),
            juvenile_female=int(string_to_number(
                self.row_value(row, COUNT_JUVENILE_FEMALES))),
            sub_adult_total=int(string_to_number(
                self.row_value(row, COUNT_SUBADULT_TOTAL))),
            sub_adult_male=int(string_to_number(
                self.row_value(row, COUNT_SUBADULT_MALE))),
            sub_adult_female=int(string_to_number(
                self.row_value(row, COUNT_SUBADULT_FEMALE))),
            juvenile_total=int(string_to_number(
                self.row_value(row, COUNT_JUVENILE_TOTAL))),
            group=int(string_to_number(self.row_value(row, GROUP))),
            open_close_system=open_close_system,
            survey_method=survey_method,
            presence=string_to_boolean(presence),
            upper_confidence_level=float(string_to_number(
                self.row_value(row, UPPER))),
            lower_confidence_level=float(string_to_number(
                self.row_value(row, LOWER))),
            certainty_of_bounds=int(string_to_number(
                self.row_value(row, CERTAINTY_OF_POPULATION))),
            sampling_effort_coverage=self.sampling_effort(row),
            population_estimate_certainty=int(string_to_number(pop_certainty)),
            population_estimate_category=population_estimate,
            survey_method_other=sur_other,
            population_estimate_category_other=pop_other
        )

        if annual_created:
            self.created_list += 1
        else:
            self.existed_list += 1

        # Save AnnualPopulationPerActivity translocation intake
        if self.row_value(row, INTRODUCTION_TOTAL):
            take, in_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Translocation (Intake)"),
                year=int(string_to_number(year)),
                owned_species=owned_species,
                total=int(string_to_number(
                    self.row_value(row, INTRODUCTION_TOTAL))),
                adult_male=int(string_to_number(
                    self.row_value(row, INTRODUCTION_TOTAL_MALES))),
                adult_female=int(string_to_number(
                    self.row_value(row, INTRODUCTION_TOTAL_FEMALES))),
                juvenile_male=int(string_to_number(
                    self.row_value(row, INTRODUCTION_MALE_JUV))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, INTRODUCTION_FEMALE_JUV))),
                reintroduction_source=self.row_value(
                    row, INTRODUCTION_SOURCE),
                founder_population=string_to_boolean(
                    self.row_value(row, FOUNDER_POPULATION)),
                intake_permit=self.row_value(row, INTRODUCTION_PERMIT_NUMBER)
            )

        # Save AnnualPopulationPerActivity translocation offtake
        if self.row_value(row, TRANS_OFFTAKE_TOTAL):
            off, off_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Translocation (Offtake)"),
                year=int(string_to_number(year)),
                owned_species=owned_species,
                total=int(string_to_number(
                    self.row_value(row, TRANS_OFFTAKE_TOTAL))),
                adult_male=int(string_to_number(
                    self.row_value(row, TRANS_OFFTAKE_ADULTE_MALES))),
                adult_female=int(string_to_number(
                    self.row_value(row, TRANS_OFFTAKE_ADULTE_FEMALES))),
                juvenile_male=int(string_to_number(
                    self.row_value(row, TRANS_OFFTAKE_MALE_JUV))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, TRANS_OFFTAKE_FEMALE_JUV))),
                translocation_destination=self.row_value(
                    row, TRANS_DESTINATION),
                offtake_permit=self.row_value(row, TRANS_OFFTAKE_PERMIT_NUMBER)
            )

        # Save AnnualPopulationPerActivity Planned hunt/cull
        if self.row_value(row, PLANNED_HUNT_TOTAL):
            h, hunt_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Planned Hunt/Cull"),
                year=int(string_to_number(year)),
                owned_species=owned_species,
                total=int(string_to_number(
                    self.row_value(row, PLANNED_HUNT_TOTAL))),
                adult_male=int(string_to_number(
                    self.row_value(row, PLANNED_HUNT_OFFTAKE_ADULT_MALES))),
                adult_female=int(string_to_number(
                    self.row_value(row, PLANNED_HUNT_OFFTAKE_ADULT_FAMALES))),
                juvenile_male=int(string_to_number(
                    self.row_value(row, PLANNED_HUNT_OFFTAKE_MALE_JUV))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, PLANNED_HUNT_OFFTAKE_FEMALE_JUV))),
                offtake_permit=self.row_value(row, PLANNED_HUNT_PERMIT_NUMBER),
            )

        # Save AnnualPopulationPerActivity Planned euthanasia
        if self.row_value(row, PLANNED_EUTH_TOTAL):
            pe, pe_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Planned Euthanasia/DCA"),
                year=int(string_to_number(year)),
                owned_species=owned_species,
                total=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_TOTAL))),
                adult_male=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_OFFTAKE_ADULT_MALES))),
                adult_female=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_OFFTAKE_ADULT_FAMALES))),
                juvenile_male=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_OFFTAKE_MALE_JUV))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_OFFTAKE_FEMALE_JUV))),
                offtake_permit=self.row_value(
                    row, PLANNED_EUTH_PERMIT_NUMBER),
            )

        # Save AnnualPopulationPerActivity Unplanned/illegal hunting
        if self.row_value(row, UNPLANNED_HUNT_TOTAL):
            unp, unp_c = AnnualPopulationPerActivity.objects.get_or_create(
                activity_type=ActivityType.objects.get(
                    name="Unplanned/Illegal Hunting"),
                year=int(string_to_number(year)),
                owned_species=owned_species,
                total=int(string_to_number(
                    self.row_value(row, UNPLANNED_HUNT_TOTAL))),
                adult_male=int(string_to_number(
                    self.row_value(row, UNPLANNED_HUNT_OFFTAKE_ADULT_MALES))),
                adult_female=int(string_to_number(
                    self.row_value(row, UNPLANNED_HUNT_OFFTAKE_ADULT_FAMALES))
                ),
                juvenile_male=int(string_to_number(
                    self.row_value(row, UNPLANNED_HUNT_OFFTAKE_MALE_JUV))),
                juvenile_female=int(string_to_number(
                    self.row_value(row, PLANNED_EUTH_OFFTAKE_FEMALE_JUV))),
                offtake_permit=self.row_value(
                    row, UNPLANNED_HUNT_OFFTAKE_FEMALE_JUV),
            )
