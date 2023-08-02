from django.db.models import F, Sum
from population_data.models import AnnualPopulation
from rest_framework import serializers
from species.models import OwnedSpecies, Taxon


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
        
        annual_populations = (
            AnnualPopulation.objects.filter(
                owned_species__taxon=obj,
            )
            .values("population_status__name")
            .annotate(population_status_total=Sum("total"))
            .values("population_status__name", "population_status_total")
        )
        return list(annual_populations)

class ActivityMatrixSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = [
            "total",
            "species_name",
            "icon",
            "activities",
        ]

    def get_total(self, obj):
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        owned_species = OwnedSpecies.objects.values(
            "taxon__common_name_varbatim").filter(taxon=obj)
        if property_list:
            owned_species = owned_species.filter(
                property__name__in=property_list,
            )
        owned_species = owned_species.annotate(
            total=Sum("annualpopulationperactivity__total")
        )
        if owned_species.exists():
            return owned_species.first()["total"]
        else:
            return None

    def get_species_name(self, obj):
        return obj.common_name_varbatim

    def get_activities(self, obj):
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        owned_species = OwnedSpecies.objects.values(
            "taxon__common_name_varbatim"
        ).filter(taxon=obj)

        if property_list:
            owned_species = owned_species.filter(
                property__name__in=property_list
            )

        owned_species = owned_species.annotate(
            total=Sum("annualpopulationperactivity__total")
        ).values("annualpopulationperactivity__activity_type__name", "total")

        total_count = self.get_total(obj)
        activities_list = []

        for item in owned_species:
            activity_type = item[
                "annualpopulationperactivity__activity_type__name"
            ]
            total = item["total"]

            if activity_type and total:
                percentage = (
                    total / total_count
                ) * 100 if total_count else None
                activity_data = {activity_type: percentage}
                activities_list.append(activity_data)

        return activities_list
