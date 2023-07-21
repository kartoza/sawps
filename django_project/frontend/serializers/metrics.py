from rest_framework import serializers
from population_data.models import AnnualPopulation
from species.models import Taxon, OwnedSpecies
from django.db.models import Sum, F



class SpeciesPopulationCountSerializer(serializers.ModelSerializer):
    specie_name = serializers.SerializerMethodField()
    specie_colour = serializers.SerializerMethodField()
    annualpopulation_count = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = [
            'specie_name',
            'specie_colour',
            'annualpopulation_count',
        ]

    def get_specie_name(self, obj):
        return obj.common_name_varbatim

    def get_specie_colour(self, obj):
        return obj.colour

    def get_annualpopulation_count(self, obj):
        months = self.context['request'].GET.get('month')
        owned_species = OwnedSpecies.objects.filter(taxon=obj)
        annual_populations = AnnualPopulation.objects.filter(
            owned_species__in=owned_species,
            month__name__in=months.split(',') if months else F('month__name')
        ).values('month').annotate(month_total=Sum('total'))
        return annual_populations
