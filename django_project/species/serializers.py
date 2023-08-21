from django.db.models import Sum
from rest_framework import serializers
from species.models import Taxon
from population_data.models import AnnualPopulation


class TaxonSerializer(serializers.ModelSerializer):
    """Species serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TaxonSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta():
        model = Taxon
        fields = '__all__'


class FrontPageTaxonSerializer(serializers.ModelSerializer):
    """Display species data on FrontPage."""
    species_name = serializers.CharField(source='scientific_name')
    total_population = serializers.SerializerMethodField()
    population_growth = serializers.SerializerMethodField()
    population_loss = serializers.SerializerMethodField()

    def get_total_population(self, obj: Taxon):
        # get latest year from current species
        latest_data_per_year = AnnualPopulation.objects.filter(
            owned_species__taxon=obj
        ).order_by(
            'owned_species__property', '-year'
        ).distinct(
            'owned_species__property'
        )
        data = AnnualPopulation.objects.filter(
            id__in=latest_data_per_year,
            owned_species__taxon=obj
        ).aggregate(Sum('total'))
        return data['total__sum'] if data['total__sum'] else 0

    def get_population_growth(self, obj: Taxon):
        # TODO: calculate population growth
        return 100

    def get_population_loss(self, obj: Taxon):
        # TODO: calculate population loss
        return 200


    class Meta:
        model = Taxon
        fields = [
            'id',
            'species_name',
            'icon',
            'total_population',
            'population_growth',
            'population_loss',
            'colour'
        ]
