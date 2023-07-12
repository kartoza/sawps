from rest_framework import serializers

from species.models import OwnedSpecies
from frontend.serializers.property import PropertySerializer
from species.serializers import TaxonSerializer
from population_data.serializers import (
    AnnualPopulationSerializer,
    AnnualPopulationPerActivitySerializer,
)


class OwnedSpeciesSerializer(serializers.ModelSerializer):
    taxon = serializers.SerializerMethodField()
    property = serializers.SerializerMethodField()
    annualpopulation = serializers.SerializerMethodField()
    annualpopulation_per_activity = serializers.SerializerMethodField()


    class Meta:
        model = OwnedSpecies
        fields = [
            'taxon',
            'property',
            'annualpopulation',
            'annualpopulation_per_activity'
        ]

    def get_taxon(self, obj):
        obj = obj.taxon
        serializer = TaxonSerializer(obj, remove_fields = ['id'])
        return serializer.data

    def get_property(self, obj):
        obj = obj.property
        serializer = PropertySerializer(
            obj,
            remove_fields = [
                'organisation_id',
                'organisation',
                'property_type_id',
                'province_id'
            ]
        )
        return serializer.data

    def get_annualpopulation(self, obj):
        request = self.context.get('request', None)
        month = request.GET.get('month')
        month = month.split(',') if month else None
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')

        queryset = obj.annualpopulation_set

        if start_year and end_year:
            if month:
                queryset = queryset.filter(
                    month__name__in=month,
                    year__range=(start_year, end_year)
                )
            else:
                queryset = queryset.filter(
                    year__range=(start_year, end_year)
                )

        serializer = AnnualPopulationSerializer(
            queryset.first(),
            remove_fields=['id', 'owned_species'],
        )
        return serializer.data

    def get_annualpopulation_per_activity(self, obj):
        request = self.context.get('request', None)
        month = request.GET.get('month')
        month = month.split(',') if month else None
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')

        queryset = obj.annualpopulationperactivity_set

        if start_year and end_year:
            if month:
                queryset = queryset.filter(
                    month__name__in=month,
                    year__range=(start_year, end_year)
                )
            else:
                queryset = queryset.filter(
                    year__range=(start_year, end_year)
                )

        serializer = AnnualPopulationPerActivitySerializer(
            queryset.first(),
            remove_fields=['id', 'owned_species'],
        )
        return serializer.data
