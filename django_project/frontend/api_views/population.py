# -*- coding: utf-8 -*-

"""API Views related to uploading population data.
"""
from datetime import datetime

from activity.models import ActivityType
from activity.serializers import ActivityTypeSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from frontend.models.upload import DraftSpeciesUpload
from occurrence.models import SamplingSizeUnit, SurveyMethod
from occurrence.serializers import (
    SamplingSizeUnitMetadataSerializer,
    SurveyMethodSerializer
)
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    CountMethod,
    OpenCloseSystem,
)
from population_data.serializers import (
    CountMethodSerializer,
    OpenCloseSystemSerializer
)
from property.models import Property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import OwnedSpecies, Taxon
from species.serializers import TaxonSerializer
from stakeholder.models import OrganisationUser


class PopulationMetadataList(APIView):
    """Get metadata for uploading population."""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        taxons = Taxon.objects.all().order_by("scientific_name")
        open_close_systems = OpenCloseSystem.objects.all().order_by("name")
        survey_methods = SurveyMethod.objects.all().order_by("name")
        sampling_size_units = SamplingSizeUnit.objects.all().order_by("unit")
        count_methods = CountMethod.objects.all().order_by("name")
        intake_events = ActivityType.objects.filter(
            recruitment=True).order_by("name")
        offtake_events = ActivityType.objects.filter(
            Q(recruitment=False) | Q(recruitment__isnull=True)
        ).order_by("name")
        return Response(
            status=200,
            data={
                "taxons": TaxonSerializer(taxons, many=True).data,
                "open_close_systems": (OpenCloseSystemSerializer(
                    open_close_systems, many=True).data
                                       ),
                "survey_methods": (
                    SurveyMethodSerializer(survey_methods, many=True).data
                ),
                "sampling_size_units": (SamplingSizeUnitMetadataSerializer(
                    sampling_size_units, many=True).data
                                        ),
                "count_methods": CountMethodSerializer(
                    count_methods, many=True).data,
                "intake_events": (
                    ActivityTypeSerializer(intake_events, many=True).data
                ),
                "offtake_events": (
                    ActivityTypeSerializer(offtake_events, many=True).data
                ),
            },
        )


class UploadPopulationAPIVIew(APIView):
    """Save new upload of population data."""

    permission_classes = [IsAuthenticated]

    def can_add_data(self, property: Property):
        # check if user belongs to organisation of property
        if self.request.user.is_superuser:
            return True
        return OrganisationUser.objects.filter(
            organisation=property.organisation, user=self.request.user
        ).exists()

    def check_existing_data(self, property: Property, taxon: Taxon, year):
        # check if no data exist for taxon+property+year
        return AnnualPopulation.objects.filter(
            year=year, owned_species__property=property,
            owned_species__taxon=taxon
        ).exists()

    def post(self, request, *args, **kwargs):
        taxon_id = request.data.get("taxon_id")
        property_id = kwargs.get("property_id")
        year = request.data.get("year")
        property = get_object_or_404(Property, id=property_id)
        taxon = get_object_or_404(Taxon, id=taxon_id)
        # validate can add data
        if not self.can_add_data(property):
            return Response(
                status=403,
                data={
                    "detail": (
                        "You cannot add data to property that "
                        "does not belong to your organisations!"
                    )
                },
            )
        if self.check_existing_data(property, taxon, year):
            return Response(
                status=400,
                data={
                    "detail": (
                        "There is already existing data "
                        f"for {taxon.scientific_name} in year {year}!"
                    )
                },
            )
        annual_population = request.data.get("annual_population")
        intake_population = request.data.get("intake_population")
        offtake_population = request.data.get("offtake_population")
        # get survey_method
        survey_method = get_object_or_404(
            SurveyMethod, id=annual_population.get("survey_method_id", 0)
        )
        # get count_method
        count_method = get_object_or_404(
            CountMethod, id=annual_population.get("count_method_id", 0)
        )
        # get sampling_size_unit
        sampling_size_unit = get_object_or_404(
            SamplingSizeUnit, id=annual_population.get(
                "sampling_size_unit_id", 0)
        )
        # get open_close_system
        open_close_system = get_object_or_404(
            OpenCloseSystem, id=annual_population.get("open_close_id")
        )
        # get intake activity
        intake_activity = get_object_or_404(
            ActivityType, id=intake_population.get("activity_type_id", 0)
        )
        # get offtake activity
        offtake_activity = get_object_or_404(
            ActivityType, id=offtake_population.get("activity_type_id", 0)
        )
        # area_available_to_species
        area_available_to_species = annual_population.get(
            "area_available_to_species", 0
        )
        # get or create owned species
        owned_species, is_new = OwnedSpecies.objects.get_or_create(
            taxon=taxon,
            property=property,
            defaults={
                "user": self.request.user,
                "area_available_to_species": area_available_to_species,
            },
        )
        if not is_new:
            owned_species.area_available_to_species = area_available_to_species
            owned_species.save()
        # add annual population
        AnnualPopulation.objects.create(
            year=year,
            owned_species=owned_species,
            total=annual_population.get("total"),
            adult_male=annual_population.get("adult_male", 0),
            adult_female=annual_population.get("adult_female", 0),
            juvenile_male=annual_population.get("juvenile_male", 0),
            juvenile_female=annual_population.get("juvenile_female", 0),
            area_covered=annual_population.get("area_covered", 0),
            sampling_effort=annual_population.get("sampling_effort", 0),
            group=annual_population.get("group", 0),
            note=annual_population.get("note", None),
            survey_method=survey_method,
            count_method=count_method,
            sampling_size_unit=sampling_size_unit,
            open_close_system=open_close_system,
            sub_adult_male=annual_population.get("sub_adult_male", 0),
            sub_adult_female=annual_population.get("sub_adult_female", 0),
            sub_adult_total=(annual_population.get("sub_adult_male", 0) +
                             annual_population.get("sub_adult_female", 0)
                             ),
            juvenile_total=(annual_population.get("juvenile_male", 0) +
                            annual_population.get("juvenile_female", 0)
                            ),
        )
        # add annual population per activity - intake
        AnnualPopulationPerActivity.objects.create(
            year=year,
            owned_species=owned_species,
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
            intake_permit=intake_population.get("permit_number", None),
        )
        # add annual population per activity - offtake
        AnnualPopulationPerActivity.objects.create(
            year=year,
            owned_species=owned_species,
            activity_type=offtake_activity,
            total=offtake_population.get("total"),
            adult_male=offtake_population.get("adult_male", 0),
            adult_female=offtake_population.get("adult_female", 0),
            juvenile_male=offtake_population.get("juvenile_male", 0),
            juvenile_female=offtake_population.get("juvenile_female", 0),
            intake_permit=offtake_population.get("permit_number", None),
        )
        # TODO: missing field translocation_destination
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
