"""API Views related to uploading population data.
"""
from datetime import datetime
from statistics import mean, stdev

from activity.models import ActivityType
from activity.serializers import ActivityTypeSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from frontend.api_views.metrics import BasePropertyCountAPIView
from frontend.models.upload import DraftSpeciesUpload
from frontend.serializers.population import (
    AnnualPopulationFormSerializer,
    ActivityFormSerializer
)
from occurrence.models import SurveyMethod
from occurrence.serializers import SurveyMethodSerializer
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    PopulationEstimateCategory,
    PopulationStatus,
    SamplingEffortCoverage,
)
from population_data.serializers import (
    PopulationEstimateCategorySerializer,
    PopulationStatusSerializer,
    SamplingEffortCoverageSerializer,
)
from property.models import Property, PropertyType
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import Taxon
from species.serializers import TaxonSerializer
from stakeholder.models import OrganisationUser
from frontend.utils.statistical_model import (
    mark_model_output_as_outdated_by_species_list
)



class PopulationMetadataList(APIView):
    """Get metadata for uploading population."""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        # filter only taxon with rank species
        taxons = Taxon.objects.filter(
            taxon_rank__name__iexact="species"
        ).order_by('scientific_name')
        survey_methods = SurveyMethod.objects.all().order_by("name")
        intake_events = ActivityType.objects.filter(
            recruitment=True).order_by("name")
        offtake_events = ActivityType.objects.filter(
            Q(recruitment=False) | Q(recruitment__isnull=True)
        ).order_by("name")
        sampling_effort_coverages = (
            SamplingEffortCoverage.objects.all().order_by("name")
        )
        population_statuses = PopulationStatus.objects.all().order_by("name")
        population_estimate_categories = (
            PopulationEstimateCategory.objects.all().order_by("name")
        )
        return Response(
            status=200,
            data={
                "taxons": TaxonSerializer(taxons, many=True).data,
                "survey_methods": (
                    SurveyMethodSerializer(survey_methods, many=True).data
                ),
                "intake_events": (
                    ActivityTypeSerializer(intake_events, many=True).data
                ),
                "offtake_events": (
                    ActivityTypeSerializer(offtake_events, many=True).data
                ),
                "sampling_effort_coverages": (
                    SamplingEffortCoverageSerializer(
                        sampling_effort_coverages, many=True
                    ).data
                ),
                "population_statuses": (
                    PopulationStatusSerializer(
                        population_statuses, many=True
                    ).data
                ),
                "population_estimate_categories": (
                    PopulationEstimateCategorySerializer(
                        population_estimate_categories, many=True
                    ).data
                )
            },
        )


class CanWritePopulationData(APIView):
    """API to check whether user can update the data."""

    permission_classes = [IsAuthenticated]
    ADD_DATA_NO_PERMISSION_MESSAGE = (
        "You cannot add data to property that "
        "does not belong to your organisations!"
    )
    EDIT_DATA_NO_PERMISSION_MESSAGE = (
        "You cannot edit data that does not belong to you!"
    )
    EDIT_DATA_NO_PERMISSION_OVERWRITE_MESSAGE = (
        "There is existing population data at year {} for this property. "
        "You are not allowed to edit data that does not belong to you!"
    )
    EDIT_DATA_CONFIRM_OVERWRITE_MESSAGE = (
        "There is existing population data at year {} for this property. "
        "Are you sure to overwrite the other data?"
    )

    def can_add_data(self, property: Property):
        # check if user belongs to organisation of property
        if self.request.user.is_superuser:
            return True
        return OrganisationUser.objects.filter(
            organisation=property.organisation, user=self.request.user
        ).exists()

    def can_overwrite_data(self, annual_population: AnnualPopulation,
                           property: Property, taxon: Taxon):
        """Check if user is able to overwrite annual_population record."""
        user = self.request.user
        if not annual_population.is_editable(user):
            return False, self.EDIT_DATA_NO_PERMISSION_MESSAGE, None
        annual_population_id = self.request.data.get('id', 0)
        year = self.request.data.get("year")
        other = None
        if annual_population_id == 0:
            other = annual_population
        elif year != annual_population.year:
            # find other annual_population in the updated year
            other = AnnualPopulation.objects.filter(
                year=year,
                taxon=taxon,
                property=property
            ).first()
        if other:
            # when there is existing data in that year,
            # check whether user is also able to edit that data
            if not other.is_editable(user):
                msg = (
                    self.EDIT_DATA_NO_PERMISSION_OVERWRITE_MESSAGE.format(
                        year)
                )
                return False, msg, other
            msg = self.EDIT_DATA_CONFIRM_OVERWRITE_MESSAGE.format(year)
            return True, msg, other
        return True, None, None

    def find_existing_annual_population(self, taxon, property):
        annual_population_id = self.request.data.get('id', 0)
        annual_population = None
        if annual_population_id == 0:
            annual_population = AnnualPopulation.objects.filter(
                year=self.request.data.get("year"),
                taxon=taxon,
                property=property,
            ).first()
        else:
            annual_population = get_object_or_404(
                AnnualPopulation, id=annual_population_id)
        return annual_population

    def post(self, request, *args, **kwargs):
        property_id = kwargs.get("property_id")
        property_obj = get_object_or_404(Property, id=property_id)
        taxon_id = request.data.get("taxon_id")
        taxon = get_object_or_404(Taxon, id=taxon_id)
        annual_population = self.find_existing_annual_population(
            taxon, property_obj)
        if annual_population is None:
            if not self.can_add_data(property_obj):
                return Response(
                    status=403,
                    data={
                        "detail": self.ADD_DATA_NO_PERMISSION_MESSAGE
                    },
                )
        else:
            can_edit, message, other = (
                self.can_overwrite_data(
                    annual_population, property_obj, taxon)
            )
            if not can_edit:
                return Response(
                    status=403,
                    data={
                        "detail": message
                    }
                )
            elif message:
                return Response(
                    status=200,
                    data={
                        "detail": message,
                        "other_id": other.id
                    }
                )
        return Response(
            status=200,
            data={
                "detail": "OK"
            }
        )


class UploadPopulationAPIVIew(CanWritePopulationData):
    """Save new upload of population data."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        taxon_id = request.data.get("taxon_id")
        property_id = kwargs.get("property_id")
        year = request.data.get("year")
        if year > timezone.now().year:
            return Response(
                status=400,
                data={
                    "detail": (
                        "Year should not exceed current year!"
                    )
                },
            )
        property_obj = get_object_or_404(Property, id=property_id)
        taxon = get_object_or_404(Taxon, id=taxon_id)
        annual_population = request.data.get("annual_population")
        intake_populations = request.data.get("intake_populations")
        offtake_populations = request.data.get("offtake_populations")
        # get survey_method
        survey_method = get_object_or_404(
            SurveyMethod, id=annual_population.get("survey_method_id", 0)
        )
        # area_available_to_species
        area_available_to_species = annual_population.get(
            "area_available_to_species", 0
        )
        sampling_effort_coverage = None
        sampling_effort_coverage_id = annual_population.get(
            "sampling_effort_coverage_id", None)
        if sampling_effort_coverage_id:
            sampling_effort_coverage = get_object_or_404(
                SamplingEffortCoverage, id=sampling_effort_coverage_id
            )
        population_status = None
        population_status_id = annual_population.get(
            "population_status_id", None)
        if population_status_id:
            population_status = get_object_or_404(
                PopulationStatus, id=population_status_id
            )
        population_estimate_category = None
        population_estimate_category_id = annual_population.get(
            "population_estimate_category_id", None)
        if population_estimate_category_id:
            population_estimate_category = get_object_or_404(
                PopulationEstimateCategory, id=population_estimate_category_id
            )
        # build update fields
        updated_fields = {
            'year': year,
            'user': self.request.user,
            'area_available_to_species': area_available_to_species,
            'total': annual_population.get("total"),
            'adult_total': annual_population.get("adult_total", 0),
            'adult_male': annual_population.get("adult_male", 0),
            'adult_female': annual_population.get("adult_female", 0),
            'juvenile_male': annual_population.get(
                "juvenile_male", 0),
            'juvenile_female': annual_population.get(
                "juvenile_female", 0),
            'group': annual_population.get("group", 0),
            'note': annual_population.get("note", None),
            'survey_method': survey_method,
            'sub_adult_male': annual_population.get(
                "sub_adult_male", 0),
            'sub_adult_female': annual_population.get(
                "sub_adult_female", 0),
            'sub_adult_total': (
                annual_population.get("sub_adult_male", 0) +
                annual_population.get("sub_adult_female", 0)),
            'juvenile_total': (
                annual_population.get("juvenile_male", 0) +
                annual_population.get("juvenile_female", 0)),
            'population_estimate_certainty': annual_population.get(
                "population_estimate_certainty", None),
            'upper_confidence_level': annual_population.get(
                "upper_confidence_level", None),
            'lower_confidence_level': annual_population.get(
                "lower_confidence_level", None),
            'certainty_of_bounds': annual_population.get(
                "certainty_of_bounds", None),
            'population_estimate_category_other': (
                annual_population.get(
                    "population_estimate_category_other", None)),
            'survey_method_other': annual_population.get(
                "survey_method_other", None),
            'population_status': population_status,
            'population_estimate_category': (
                population_estimate_category),
            'sampling_effort_coverage': sampling_effort_coverage,
            'presence': annual_population.get("present")
        }
        # validate permission for creating/updating population data
        annual_population_obj = self.find_existing_annual_population(
            taxon, property_obj)
        if annual_population_obj is None:
            # validate can add new population data
            if not self.can_add_data(property_obj):
                return Response(
                    status=403,
                    data={
                        "detail": self.ADD_DATA_NO_PERMISSION_MESSAGE
                    },
                )
            updated_fields['taxon'] = taxon
            updated_fields['property'] = property_obj
            annual_population_obj = (
                AnnualPopulation.objects.create(**updated_fields)
            )
        else:
            can_edit, message, other = (
                self.can_overwrite_data(
                    annual_population_obj, property_obj, taxon)
            )
            if not can_edit:
                return Response(
                    status=403,
                    data={
                        "detail": message
                    }
                )
            confirm_overwrite = request.data.get('confirm_overwrite', False)
            if other and not confirm_overwrite:
                return Response(status=400, data={
                    "detail": (
                        f"Please confirm to overwrite data at year {year}"
                    )
                })
            if other and other.id != annual_population_obj.id:
                # remove the other data
                other.delete()
            AnnualPopulation.objects.filter(
                id=annual_population_obj.id
            ).update(**updated_fields)
            annual_population_obj.refresh_from_db()
            # clear existing activities data
            AnnualPopulationPerActivity.objects.filter(
                annual_population=annual_population_obj
            ).delete()
        # add annual population per activity - intake
        for intake_population in intake_populations:
            # get intake activity
            intake_activity = ActivityType.objects.filter(
                id=intake_population.get("activity_type_id", 0)
            ).first()
            if intake_activity is None:
                continue
            AnnualPopulationPerActivity.objects.create(
                year=year,
                annual_population=annual_population_obj,
                activity_type=intake_activity,
                total=intake_population.get("total"),
                adult_male=intake_population.get("adult_male", 0),
                adult_female=intake_population.get("adult_female", 0),
                juvenile_male=intake_population.get("juvenile_male", 0),
                juvenile_female=intake_population.get("juvenile_female", 0),
                founder_population=intake_population.get(
                    "founder_population", None),
                reintroduction_source=intake_population.get(
                    "reintroduction_source", None),
                intake_permit=intake_population.get("permit", None),
                note=intake_population.get("note", None),
            )
        # add annual population per activity - offtake
        for offtake_population in offtake_populations:
            # get offtake activity
            offtake_activity = ActivityType.objects.filter(
                id=offtake_population.get("activity_type_id", 0)
            ).first()
            if offtake_activity is None:
                continue
            AnnualPopulationPerActivity.objects.create(
                year=year,
                annual_population=annual_population_obj,
                activity_type=offtake_activity,
                total=offtake_population.get("total"),
                adult_male=offtake_population.get("adult_male", 0),
                adult_female=offtake_population.get("adult_female", 0),
                juvenile_male=offtake_population.get("juvenile_male", 0),
                juvenile_female=offtake_population.get("juvenile_female", 0),
                reintroduction_source=offtake_population.get(
                    "reintroduction_source", None),
                translocation_destination=offtake_population.get(
                    "translocation_destination", None),
                offtake_permit=offtake_population.get("permit", None),
                note=offtake_population.get("note", None),
            )
        # mark statistical model output as outdated
        mark_model_output_as_outdated_by_species_list([taxon.id])
        # if draft exists, then delete it
        draft_uuid = request.GET.get("uuid", None)
        if draft_uuid:
            DraftSpeciesUpload.objects.filter(uuid=draft_uuid).delete()
        return Response(status=204)


class FetchDraftPopulationUpload(APIView):
    """API to fetch draft upload."""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        draft_uuid = kwargs.get("draft_uuid")
        draft_upload = get_object_or_404(DraftSpeciesUpload, uuid=draft_uuid)
        return Response(
            status=200,
            data={
                "last_step": draft_upload.last_step,
                "form_data": draft_upload.form_data,
            },
        )

    def delete(self, request, *args, **kwargs):
        draft_uuid = kwargs.get("draft_uuid")
        draft_upload = get_object_or_404(DraftSpeciesUpload, uuid=draft_uuid)
        draft_upload.delete()
        return Response(status=204)


class DraftPopulationUpload(APIView):
    """API to fetch draft list and save as draft."""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        property_id = kwargs.get("property_id")
        property = get_object_or_404(Property, id=property_id)
        drafts = (
            DraftSpeciesUpload.objects.filter(property=property)
            .order_by("-upload_date")
            .values_list("uuid", flat=True)
        )
        return Response(status=200, data=drafts)

    def post(self, request, *args, **kwargs):
        property_id = kwargs.get("property_id")
        property = get_object_or_404(Property, id=property_id)
        draft_uuid = request.GET.get("uuid", None)
        draft_time = datetime.now()
        draft_name = request.data.get("name", None)
        if draft_name is None:
            draft_name = f'{property.name}_{draft_time.strftime("%d_%m_%y")}'
        draft: DraftSpeciesUpload
        if draft_uuid:
            draft = get_object_or_404(DraftSpeciesUpload, uuid=draft_uuid)
        else:
            draft = DraftSpeciesUpload.objects.create(
                property=property,
                name=draft_name,
                upload_by=request.user,
                upload_date=draft_time,
            )
        draft.last_step = request.data.get("last_step")
        draft.form_data = request.data.get("form_data")
        taxon_id = draft.form_data.get("taxon_id", None)
        if taxon_id:
            draft.taxon = get_object_or_404(Taxon, id=taxon_id)
        draft.year = draft.form_data.get("year", None)
        draft.upload_date = draft_time
        draft.save()
        return Response(status=201, data={"uuid": str(draft.uuid)})


class FetchPopulationData(APIView):
    """Fetch existing annual population data."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        annual_population_id = kwargs.get("id")
        annual_population = get_object_or_404(AnnualPopulation,
                                              id=annual_population_id)
        intakes = AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population,
            activity_type__recruitment=True
        ).select_related('activity_type').order_by('id')
        offtakes = AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population
        ).filter(
            Q(activity_type__recruitment__isnull=True) |
            Q(activity_type__recruitment=False)
        ).select_related('activity_type').order_by('id')
        return Response(
            status=200,
            data={
                'id': annual_population_id,
                'taxon_id': annual_population.taxon.id,
                'taxon_name': annual_population.taxon.scientific_name,
                'common_name': annual_population.taxon.common_name_verbatim,
                'year': annual_population.year,
                'property_id': annual_population.property.id,
                'annual_population': AnnualPopulationFormSerializer(
                    annual_population, many=False
                ).data,
                'intake_populations': ActivityFormSerializer(
                    intakes, many=True
                ).data,
                'offtake_populations': ActivityFormSerializer(
                    offtakes, many=True
                ).data
            }
        )


FEMALE_SUFFIX = '_female'
MALE_SUFFIX = '_male'
TOTAL_SUFFIX = '_total'


class PopulationMeanSDChartApiView(BasePropertyCountAPIView):
    """
    API view for calculating and presenting statistical data
    related to population means and standard deviations (SD)
    based on different age classes.
    """
    age_classes = ['adult', 'sub_adult', 'juvenile']

    def calculate_sd_and_mean_by_age_class(self, data, age_class: str) -> dict:
        """
        Calculates the mean and standard deviation (SD) for
        male and female data within a specified age class.

        :param data: A dictionary containing population data.
        :param age_class: The age class for which calculations are performed.
        """
        male_data = []
        female_data = []

        female_class = age_class + FEMALE_SUFFIX
        male_class = age_class + MALE_SUFFIX

        for location, years in data.items():
            for year, age_classes in years.items():
                if male_class in age_classes:
                    male_data.append(age_classes[male_class])
                if female_class in age_classes:
                    female_data.append(age_classes[female_class])

        mean_male = mean(male_data) if male_data else 0
        sd_male = stdev(male_data) if len(male_data) > 1 else 0

        mean_female = mean(female_data) if female_data else 0
        sd_female = stdev(female_data) if len(female_data) > 1 else 0

        return {
            'mean_' + female_class: mean_female,
            'sd_' + female_class: sd_female,
            'mean_' + male_class: mean_male,
            'sd_' + male_class: sd_male
        }

    def calculate_sd_and_mean(self, data) -> dict:
        """
        Aggregates mean and standard deviation calculations
            across all age classes.

        :param data: A dictionary containing detailed population data
            segregated by age classes.
        :return: A dictionary with aggregated mean and SD values for
            each age class and gender.
        """
        sd_and_means = {}
        for age_class in self.age_classes:
            sd_and_means.update(
                self.calculate_sd_and_mean_by_age_class(
                    data, age_class
                )
            )
        return sd_and_means

    def calculate_percentage(
            self,
            annual_population: AnnualPopulation, age_class: str) -> dict:
        """
        Calculates the percentage of male and female populations in a
        given age class.

        :param annual_population: object representing annual population data.
        :param age_class: age class for which the percentage
            calculation is done.
        :return: dictionary with percentage values for
            males and females in the specified age class.
        """
        age_class_male = age_class + MALE_SUFFIX
        age_class_female = age_class + FEMALE_SUFFIX
        age_class_total = age_class + TOTAL_SUFFIX
        male = getattr(annual_population, age_class_male)
        female = getattr(annual_population, age_class_female)
        total = getattr(annual_population, age_class_total)

        if not male:
            male = 0

        if not female:
            female = 0

        if not total:
            total = male + female

        return {
            age_class_male: male / total * 100 if total > 0 else 0,
            age_class_female: female / total * 100 if total > 0 else 0
        }

    def age_group_by_property_type(self, property_type: PropertyType) -> dict:
        """
        Organizes and calculates percentage distribution
        of age classes by property type.

        :param property_type: The property type for which data is organized.
        :return: A dictionary with percentage distributions for each age class,
            organized by year and property type.
        """
        annual_populations = self.get_queryset().filter(
            property__property_type=property_type
        ).order_by('year').distinct()
        year = {}

        for annual_population in annual_populations:
            if annual_population.year not in year:
                year[annual_population.year] = {}

            for age_class in self.age_classes:
                year[annual_population.year].update(
                    self.calculate_percentage(
                        annual_population,
                        age_class
                    )
                )
        return {
            property_type.name: year
        }

    def get(self, request, *args):
        """
        Handle GET request
        """
        property_types = PropertyType.objects.all()

        result = {}

        for property_type in property_types:
            result[property_type.name] = self.calculate_sd_and_mean(
                self.age_group_by_property_type(
                    property_type
                ))

        return Response(result)
