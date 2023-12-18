import datetime
from typing import List

from django.db.models import (
    F,
    Q,
    Sum,
    Exists,
    OuterRef
)
from rest_framework import serializers

from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from property.models import Property
from species.models import Taxon
from frontend.models.spatial import SpatialDataValueModel


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
        return obj.common_name_verbatim

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
        property = self.context['request'].GET.get('property')
        annual_populations = (
            AnnualPopulation.objects.filter(
                Q(
                    property__id__in=property.split(",")
                ) if property else Q(),
                taxon=obj
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
        populations = AnnualPopulation.objects.values(
            "taxon__common_name_verbatim").filter(taxon=obj)
        if property_list:
            populations = populations.filter(
                property__id__in=property_list,
            )
        populations = populations.annotate(
            total=Sum("total")
        )
        if populations.exists():
            return populations[0].get("total")
        else:
            return None

    def get_species_name(self, obj) -> str:
        """Get the species name.
        Params: obj (Taxon): The Taxon instance.
        """
        return obj.common_name_verbatim

    def get_activities(self, obj) -> List[dict]:
        """Calculate activity percentage data for species.
        Params: obj (Taxon): The Taxon instance.
        """
        property = self.context['request'].GET.get('property')
        property_list = property.split(',') if property else []
        populations = AnnualPopulation.objects.values(
            "taxon__common_name_verbatim"
        ).filter(taxon=obj)

        if property_list:
            populations = populations.filter(
                property__id__in=property_list
            )

        populations = populations.annotate(
            total=Sum("annualpopulationperactivity__total")
        ).values("annualpopulationperactivity__activity_type__name", "total")

        total_count = self.get_total(obj)
        activities_list = []

        for item in populations:
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


class TotalCountPerPopulationEstimateSerializer(serializers.Serializer):
    def get_total_counts_per_population_estimate(self):
        """
        Retrieves and calculates the total counts per
        population estimate category.

        This function filters AnnualPopulation records
        based on the provided parameters
        (species_name, property_ids).
        It then iterates through the filtered records and calculates
        the total counts per population estimate category,
        along with the most recent year and total sums associated
        with each category.

        Returns:
        - result (dict): A dictionary containing total counts per
        population estimate category.
            Each category includes count, years, total, and percentage.
        """

        # Extract filter parameters from the request context
        species_name = self.context["request"].GET.get("species")
        property_list = self.context['request'].GET.get('property')
        property_ids = property_list.split(',') if property_list else []
        activity_filter = self.context['request'].GET.get('activity', "")
        spatial_filter_values = self.context['request'].GET.get(
            'spatial_filter_values', "").split(',')
        spatial_filter_values = list(
            filter(None, spatial_filter_values)
        )

        # Initialize a dictionary to store the results
        result = {}

        start_year = self.context["request"].GET.get('start_year')
        end_year = self.context["request"].GET.get('end_year')
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            max_year = max(start_year, end_year)
        except (ValueError, TypeError):
            max_year = None  # if the input is not valid integers

        # Query AnnualPopulation model to filter records
        # for the most recent year
        annual_populations = (
            AnnualPopulation.objects.filter(
                Q(
                    property__id__in=property_ids
                ) if property_ids else Q(),
                Q(
                    Q(
                        taxon__common_name_verbatim=(
                            species_name
                        )
                    ) |
                    Q(taxon__scientific_name=species_name)
                ) if species_name else Q(),
                year=max_year,
            )
        )
        if activity_filter:
            activity_qs = AnnualPopulationPerActivity.objects.filter(
                annual_population=OuterRef('pk'),
                activity_type_id__in=[
                    int(act) for act in activity_filter.split(',')
                ]
            )
            annual_populations = annual_populations.filter(
                Exists(activity_qs))
        if spatial_filter_values:
            spatial_qs = SpatialDataValueModel.objects.filter(
                spatial_data__property=OuterRef('property'),
                context_layer_value__in=spatial_filter_values
            )
            annual_populations = annual_populations.filter(
                Exists(spatial_qs))

        # Iterate through filtered records
        for record in annual_populations:
            population_estimate_category = (
                record.population_estimate_category.name
                if record.population_estimate_category else ''
            )
            year = record.year
            total = record.total

            # Calculate percentage against the total
            percentage = (total / total) * 100 if total > 0 else 0

            # Create or update the result dictionary
            if population_estimate_category not in result:
                result[population_estimate_category] = {
                    "count": 1,
                    "years": [year],
                    "total": total,
                    "percentage": percentage * 100
                }
            elif year in result[population_estimate_category]["years"]:
                result[population_estimate_category]["count"] += 1
                result[population_estimate_category]["total"] += total
            else:
                result[population_estimate_category]["years"].append(year)
                result[population_estimate_category]["count"] += 1
                result[population_estimate_category]["total"] += total

        # Initialize a dictionary to store the final results
        final_result = {}

        # Iterate over the result again to calculate the percentages
        for category, data in result.items():
            count = data["count"]
            total = data["total"]

            # Calculate percentage as count divided by total * 100
            percentage = (count / total) * 100 if total > 0 else 0

            # Create the final result entry
            final_result[category] = {
                "count": count,
                "years": data["years"],
                "total": total,
                "percentage": int(percentage * 100) / 100,
            }

        return final_result


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
        start_year = self.context['request'].GET.get("start_year", 0)
        end_year = self.context['request'].GET.get(
            "end_year", datetime.datetime.now().year
        )
        year_range = (int(start_year), int(end_year))
        activity_filter = self.context['request'].GET.get('activity', "")
        spatial_filter = self.context['request'].GET.get(
            'spatial_filter_values', "").split(',')
        spatial_filter = list(
            filter(None, spatial_filter)
        )
        populations = AnnualPopulation.objects.values(
            "taxon__common_name_verbatim").filter(
            taxon=obj,
            year__range=year_range
        )
        if property_list:
            populations = populations.filter(
                property__id__in=property_list,
            )

        if activity_filter:
            activity_qs = AnnualPopulationPerActivity.objects.filter(
                annual_population=OuterRef('pk'),
                activity_type_id__in=[
                    int(act) for act in activity_filter.split(',')
                ]
            )
            populations = populations.filter(Exists(activity_qs))
        if spatial_filter:
            spatial_qs = SpatialDataValueModel.objects.filter(
                spatial_data__property=OuterRef('property'),
                context_layer_value__in=spatial_filter
            )
            populations = populations.filter(Exists(spatial_qs))

        populations = populations.annotate(
            total_population=Sum("total")
        )
        if populations.exists():
            return populations[0].get("total_population")
        else:
            return None

    def get_species_name(self, obj) -> str:
        """Get the species name.
        Params: obj (Taxon): The Taxon instance.
        """
        return obj.common_name_verbatim


    def get_activities(self, obj) -> List[dict]:
        """Calculate total count per activity for species.
        Params: obj (Taxon): The Taxon instance.
        """
        property_param = self.context['request'].GET.get('property')
        property_list = property_param.split(',') if property_param else []
        start_year = self.context['request'].GET.get("start_year", 0)
        end_year = self.context['request'].GET.get(
            "end_year", datetime.datetime.now().year
        )
        year_range = (int(start_year), int(end_year))
        activity_filter = self.context['request'].GET.get('activity', "")
        spatial_filter = self.context['request'].GET.get(
            'spatial_filter_values', "").split(',')
        spatial_filter = list(
            filter(None, spatial_filter)
        )

        q_filters = Q(annual_population__taxon=obj, year__range=year_range)
        if property_list:
            q_filters &= Q(annual_population__property_id__in=property_list)
        if activity_filter:
            q_filters &= Q(activity_type_id__in=[
                int(act) for act in activity_filter.split(',')
            ])
        if spatial_filter:
            spatial_qs = SpatialDataValueModel.objects.filter(
                spatial_data__property=OuterRef('annual_population__property'),
                context_layer_value__in=spatial_filter
            )
            q_filters &= Q(Exists(spatial_qs))

        populations = AnnualPopulationPerActivity.objects.filter(
            q_filters
        ).values(
            'year',
            'activity_type__name'
        ).annotate(
            activity_total=Sum('total')
        ).order_by()

        activities_list = [
            {
                "activity_type": item["activity_type__name"],
                "year": item["year"],
                "total": item["activity_total"],
            }
            for item in populations
            if item["activity_type__name"] and item["activity_total"]
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
            "organisation_name"
        ]

    def get_province_name(self, obj):
        return obj.province.name if obj.province else None

    def get_organisation_name(self, obj):
        return obj.organisation.name if obj.organisation else None

    def get_density(self, obj) -> dict:
        species_name = self.context.get("species_name")
        if not species_name:
            return None

        start_year = self.context['request'].GET.get("start_year", 0)
        end_year = self.context['request'].GET.get(
            "end_year", datetime.datetime.now().year
        )
        year_range = (int(start_year), int(end_year))

        populations = (
            AnnualPopulation.objects.filter(
                property=obj,
                taxon__scientific_name=species_name,
                year__range=year_range
            )
            .values(
                "property__name",
                "year",
                "total",
                "area_available_to_species"
            )
        )

        # Calculate density and format data
        result_data = []
        for data in populations:
            total = data.get("total")
            area_available = data.get("area_available_to_species")
            year = data.get("year")

            if total and area_available:
                density = total / area_available
            else:
                density = None

            property_name = data.get("property__name").capitalize()

            result_data.append({
                "property_name": property_name,
                "density": density,
                "species_name": species_name,
                "year": year,
            })

        return result_data


class PopulationPerAgeGroupSerialiser(serializers.ModelSerializer):
    """
    Serializer class for serializing population per age group.
    """
    age_group = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = ["age_group", "graph_icon", "common_name_verbatim", "colour"]

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
            "juvenile_female",
            "year",
            "total"
        ]

        filters = {
            "taxon": obj
        }

        property_list = self.context['request'].GET.get("property")
        if property_list:
            property_ids = property_list.split(",")
            filters["property__id__in"] = property_ids

        start_year = self.context['request'].GET.get("start_year")
        if start_year:
            end_year = self.context['request'].GET.get("end_year")
            filters["year__range"] = (start_year, end_year)

        age_groups_totals = (
            AnnualPopulation.objects
            .values("taxon__common_name_verbatim")
            .filter(**filters)
            .annotate(
                **{
                    f"total_{field}": (
                        Sum(field) if field != 'year' else F('year')
                    )
                    for field in sum_fields
                }
            )
        )

        fields = set(sum_fields).difference({'year', 'total'})
        total_unspecified = F('total_total') - sum(
            [F(f'total_{field}') for field in fields]
        )
        age_groups_totals = age_groups_totals.annotate(
            total_unspecified=
            total_unspecified if
            total_unspecified else F('total_total')
        )
        for age_group in age_groups_totals:
            if age_group['total_unspecified'] is None:
                age_group['total_unspecified'] = age_group['total_total']

        return age_groups_totals


class AnnualPopulationSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing AnnualPopulation.
    """
    class Meta:
        model = AnnualPopulation
        fields = (
            'year',
            'survey_method'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['property__province'] = (
            instance.property.province
        )
        data['property__property_type'] = (
            instance.property.property_type
        )
        return data


class TotalAreaVSAvailableAreaSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing total area and available area.
    """
    area = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = ["area", "common_name_verbatim"]

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
            filters["year__range"] = (start_year, end_year)

        populations = AnnualPopulation.objects.filter(
            **filters, taxon=obj
        ).values(
            'year'
        ).annotate(
            area_total=Sum("property__property_size_ha"),
            area_available=Sum("area_available_to_species")
        ).order_by('year')

        return populations


class AreaAvailablePerSpeciesSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField()
    property_name = serializers.SerializerMethodField()
    organisation_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()

    def get_species(self, obj: AnnualPopulation) -> str:
        return obj.taxon.scientific_name

    def get_property_name(self, obj: AnnualPopulation) -> str:
        return obj.property.name

    def get_organisation_name(self, obj: AnnualPopulation) -> str:
        return obj.property.organisation.name

    def get_province_name(self, obj: AnnualPopulation) -> str:
        return obj.property.province.name

    def get_area(self, obj: AnnualPopulation) -> str:
        return obj.area_available_to_species

    class Meta:
        model = AnnualPopulation
        fields = [
            'species', 'property_name', 'year',
            'organisation_name', 'province_name', 'area'
        ]
