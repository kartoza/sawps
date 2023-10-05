from typing import List
from frontend.static_mapping import YEAR_DATA_LIMIT
from django.db.models import F, Q, Sum
from population_data.models import AnnualPopulation
from property.models import Property
from rest_framework import serializers
from species.models import OwnedSpecies, Taxon


class SpeciesPopuationCountPerYearSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing population count per year for a species.
    """
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

    def get_species_name(self, obj: Taxon) -> str:
        """Get the common name of the species.
        Params:
            obj (Taxon): The Taxon instance representing the species.
        """
        return obj.common_name_varbatim

    def get_species_colour(self, obj: Taxon) -> str:
        """Get the color of the species.
        Params:
            obj (Taxon): The Taxon instance representing the species.
        """
        return obj.colour

    def get_annualpopulation_count(self, obj: Taxon) -> List[dict]:
        """Get the population count per year for the species.
        Params:
            obj (Taxon): The Taxon instance representing the species.
        """
        start_year = self.context["request"].GET.get("start_year")
        end_year = self.context["request"].GET.get("end_year")
        property = self.context['request'].GET.get('property')
        annual_populations = (
            AnnualPopulation.objects.filter(
                Q(
                    year__range=(start_year, end_year)
                ) if start_year and end_year else Q(),
                Q(
                    owned_species__property__id__in=property.split(",")
                ) if property else Q(),
                owned_species__taxon=obj
            )
            .values("year")
            .annotate(year_total=Sum("total"))
            .values("year", "year_total")
            .order_by("-year")[:10]
        )
        return list(annual_populations)


class ActivityMatrixSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing activity percentage data for species.
    """
    total = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = [
            "total",
            "species_name",
            "graph_icon",
            "activities",
        ]

    def get_total(self, obj) -> int:
        """Get the total count of species.
        Params: obj (Taxon): The Taxon instance.
        """
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        owned_species = OwnedSpecies.objects.values(
            "taxon__common_name_varbatim").filter(taxon=obj)
        if property_list:
            owned_species = owned_species.filter(
                property__id__in=property_list,
            )
        owned_species = owned_species.annotate(
            total=Sum("annualpopulation__total")
        )
        if owned_species.exists():
            return owned_species[0].get("total")
        else:
            return None

    def get_species_name(self, obj) -> str:
        """Get the species name.
        Params: obj (Taxon): The Taxon instance.
        """
        return obj.common_name_varbatim

    def get_activities(self, obj) -> List[dict]:
        """Calculate activity percentage data for species.
        Params: obj (Taxon): The Taxon instance.
        """
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        owned_species = OwnedSpecies.objects.values(
            "taxon__common_name_varbatim"
        ).filter(taxon=obj)

        if property_list:
            owned_species = owned_species.filter(
                property__id__in=property_list
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
                activity_data = {
                    activity_type: percentage,
                    "activity_total": total
                }
                activities_list.append(activity_data)

        return activities_list


class TotalCountPerActivitySerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing the total count per activity data.
    """
    total = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = [
            "total",
            "species_name",
            "graph_icon",
            "activities",
            "colour"
        ]

    def get_total(self, obj) -> int:
        """Get the total count of species.
        Params: obj (Taxon): The Taxon instance.
        """
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        owned_species = OwnedSpecies.objects.values(
            "taxon__common_name_varbatim").filter(taxon=obj)
        if property_list:
            owned_species = owned_species.filter(
                property__id__in=property_list,
            )
        owned_species = owned_species.annotate(
            total=Sum("annualpopulationperactivity__total")
        )
        if owned_species.exists():
            return owned_species[0].get("total")
        else:
            return None

    def get_species_name(self, obj) -> str:
        """Get the species name.
        Params: obj (Taxon): The Taxon instance.
        """
        return obj.common_name_varbatim


    def get_activities(self, obj) -> List[dict]:
        """Calculate total count per activity for species.
        Params: obj (Taxon): The Taxon instance.
        """
        property_param = self.context['request'].GET.get('property')
        property_list = property_param.split(',') if property_param else []

        q_filters = Q(taxon=obj)
        if property_list:
            q_filters &= Q(property__id__in=property_list)

        owned_species = OwnedSpecies.objects.values(
            activity_type=F(
                "annualpopulationperactivity__activity_type__name"),
            total=Sum("annualpopulationperactivity__total"),
        ).filter(q_filters)

        activities_list = [
            {item["activity_type"]: item["total"]}
            for item in owned_species
            if item["activity_type"] and item["total"]
        ]

        return activities_list


class SpeciesPopulationDensityPerPropertySerializer(
    serializers.ModelSerializer
):
    """
    Serializer class for serializing species population total and density.
    """
    density = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    organisation_name = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "density",
            "province_name",
            "organisation_name",
            "created_at"
        ]

    def get_province_name(self, obj):
        return obj.province.name if obj.province else None

    def get_organisation_name(self, obj):
        return obj.organisation.name if obj.organisation else None

    def get_density(self, obj) -> dict:
        species_name = self.context.get("species_name")
        if not species_name:
            return None

        # Use species_name in calculation
        owned_species = OwnedSpecies.objects.filter(
            property=obj,
            taxon__scientific_name=species_name
        ).annotate(
            total=Sum("annualpopulation__total"),
            property_in_ha=Sum("property__property_size_ha")
        ).values("property__name", "total", "property_in_ha")

        if owned_species.exists():
            property_in_ha = owned_species[0].get("property_in_ha")
            total = owned_species[0].get("total")
            density = (
                total / property_in_ha if total and property_in_ha else None
            )
            property_name = owned_species[0].get("property__name").capitalize()
            data = {
                "property_name": property_name,
                "density": density,
                "species_name": species_name
            }
            return data
        else:
            return None


class PopulationPerAgeGroupSerialiser(serializers.ModelSerializer):
    """
    Serializer class for serializing population per age group.
    """
    age_group = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = ["age_group", "graph_icon", "common_name_varbatim", "colour"]

    def get_age_group(self, obj) -> dict:
        """ Calculate population per age group.
        Params: obj (Taxon): The Taxon instance.
        """
        sum_fields = [
            "adult_male",
            "adult_female",
            "sub_adult_male",
            "sub_adult_female",
            "juvenile_male",
            "juvenile_female"
        ]

        filters = {
            "owned_species__taxon": obj
        }

        property_list = self.context['request'].GET.get("property")
        if property_list:
            property_ids = property_list.split(",")
            filters["owned_species__property__id__in"] = property_ids

        start_year = self.context['request'].GET.get("start_year")
        if start_year:
            end_year = self.context['request'].GET.get("end_year")
            filters["year__range"] = (start_year, end_year)

        age_groups_totals = AnnualPopulation.objects.values(
            "owned_species__taxon__common_name_varbatim"
        ).filter(**filters).annotate(
            **{f"total_{field}": Sum(field) for field in sum_fields}
        )

        return age_groups_totals


class TotalAreaVSAvailableAreaSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing total area and available area.
    """
    area = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = ["area", "common_name_varbatim"]

    def get_area(self, obj) -> list:
        """ Calculate and get total area and available area.
        Params: obj (Taxon): The Taxon instance.
        """

        filters = {}
        property_list = self.context['request'].GET.get("property")
        if property_list:
            property_ids = property_list.split(",")
            filters["property__id__in"] = property_ids

        start_year = self.context['request'].GET.get("start_year")
        if start_year:
            end_year = self.context['request'].GET.get("end_year")
            filters["annualpopulation__year__range"] = (start_year, end_year)

        owned_species = OwnedSpecies.objects.values(
            "annualpopulation__year",
        ).filter(**filters, taxon=obj).annotate(
            area_total=Sum("property__property_size_ha"),
            area_available=Sum("area_available_to_species")
        )
        data = {
            "owned_species": owned_species
        }
        if len(owned_species) > YEAR_DATA_LIMIT:
            data = {
                "owned_species": owned_species[:YEAR_DATA_LIMIT],
                "message": "Only last 10 years data are displayed \
                for search with >10 years data returned"
            }

        return data
