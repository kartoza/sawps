"""API Views related to uploading population data."""
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from species.models import Taxon
from species.serializers import TaxonSerializer
from activity.models import ActivityType
from activity.serializers import ActivityTypeSerializer
from occurrence.models import SamplingSizeUnit, SurveyMethod
from occurrence.serializers import (
    SamplingSizeUnitSerializer,
    SurveyMethodSerializer
)
from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    CountMethod,
    OpenCloseSystem
)
from population_data.serializers import (
    CountMethodSerializer,
    OpenCloseSystemSerializer
)


class PopulationMetadataList(APIView):
    """Get metadata for uploading population."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        taxons = Taxon.objects.all().order_by('scientific_name')
        open_close_systems = OpenCloseSystem.objects.all().order_by('name')
        survey_methods = SurveyMethod.objects.all().order_by('name')
        sampling_size_units = SamplingSizeUnit.objects.all().order_by('unit')
        count_methods = CountMethod.objects.all().order_by('name')
        intake_events = ActivityType.objects.filter(
            recruitment=True
        ).order_by('name')
        offtake_events = ActivityType.objects.filter(
            Q(recruitment=False) | Q(recruitment__isnull=True)
        ).order_by('name')
        return Response(
            status=200,
            data={
                'taxons': TaxonSerializer(taxons, many=True).data,
                'open_close_systems': (
                    OpenCloseSystemSerializer(
                        open_close_systems,
                        many=True
                    ).data
                ),
                'survey_methods': (
                    SurveyMethodSerializer(survey_methods, many=True).data
                ),
                'sampling_size_units': (
                    SamplingSizeUnitSerializer(
                        sampling_size_units,
                        many=True
                    ).data
                ),
                'count_methods': (
                    CountMethodSerializer(count_methods, many=True).data
                ),
                'intake_events': (
                    ActivityTypeSerializer(intake_events, many=True).data
                ),
                'offtake_events': (
                    ActivityTypeSerializer(offtake_events, many=True).data
                )
            }
        )


class UploadPopulationAPIVIew(APIView):
    """Save new upload of population data."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response(status=204)
