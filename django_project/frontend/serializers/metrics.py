from django.db.models import F, Sum
from population_data.models import AnnualPopulation
from rest_framework import serializers
from species.models import Taxon


class SpeciesPopulationCountSerializer(serializers.ModelSerializer):
    species_name = serializers.SerializerMethodField()
    species_colour = serializers.SerializerMethodField()
    annualpopulation_count = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = [
            "species_name",
            "species_colour",
            "annualpopulation_count",
        ]

    def get_species_name(self, obj):
        return obj.common_name_varbatim

    def get_species_colour(self, obj):
        return obj.colour

    def get_annualpopulation_count(self, obj):
        months = self.context["request"].GET.get("month")
        annual_populations = (
            AnnualPopulation.objects.filter(
                owned_species__taxon=obj,
                month__name__in=(
                    months.split(",") if months else F("month__name")
                )
            )
            .values("month__name")
            .annotate(month_total=Sum("total"))
            .values("month__name", "month_total")
        )
        return list(annual_populations)
