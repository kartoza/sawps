# Generated by Django 4.1.13 on 2023-12-04 12:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sawps", "0007_alter_extendedgroup_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="extendedgroup",
            options={
                "permissions": [
                    ("can_view_population_trend", "Can view population trend"),
                    ("can_view_population_category", "Can view population category"),
                    ("can_view_property_type", "Can view property type"),
                    ("can_view_density_bar", "Can view density bar"),
                    ("can_view_property_available", "Can view property available"),
                    ("can_view_age_group", "Can view age group"),
                    ("can_view_area_available", "Can view area available"),
                    (
                        "can_view_province_species_count",
                        "Can view province species count",
                    ),
                    (
                        "can_view_province_species_count_as_percentage",
                        "Can view province species count as percentage",
                    ),
                    ("can_view_total_count", "Can view total count"),
                    ("can_view_count_as_percentage", "Can view count as percentage"),
                    ("can_view_population_estimate", "Can view population estimate"),
                    (
                        "can_view_population_estimate_as_percentage",
                        "Can view population estimate as percentage",
                    ),
                    (
                        "can_view_map_province_layer",
                        "Can view province layer in the map",
                    ),
                    (
                        "can_view_map_properties_layer",
                        "Can view properties layer in the map",
                    ),
                    ("can_view_sampling_report", "Can view sampling report"),
                    ("can_view_province_report", "Can view province report"),
                    ("can_view_organisation_filter", "Can view organisation filter"),
                    ("can_view_property_filter", "Can view property filter"),
                    (
                        "can_view_property_count_per_area_category",
                        "Can view property count per area category",
                    ),
                    (
                        "can_view_property_count_per_area_available_to_species_category",
                        "Can view property count per area available to species category",
                    ),
                    (
                        "can_view_property_count_per_population_density_category",
                        "Can view property count per population density category",
                    ),
                    (
                        "can_edit_species_population_data",
                        "Can edit species population data",
                    ),
                    (
                        "can_view_report_as_data_consumer",
                        "Can view report as data consumer",
                    ),
                    (
                        "can_view_report_as_provincial_data_consumer",
                        "Can view report as provincial data consumer",
                    ),
                ]
            },
        ),
    ]