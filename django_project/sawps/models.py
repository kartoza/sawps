from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


PERM_CAN_ADD_SPECIES_POPULATION_DATA = (
    'Can add species population data'
)

PERM_CAN_CHANGE_DATA_USE = (
    'Can change data use permissions'
)


class ExtendedGroup(models.Model):
    """
    Stores additional attributes for Django's built-in Group model.
    Related to :model:`auth.Group`.
    """

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='extended')

    description = models.TextField()

    def __str__(self):
        return self.description

    class Meta:
        permissions = [
            ("can_view_population_trend", "Can view population trend"),
            ("can_view_population_category", "Can view population category"),
            ("can_view_property_type", "Can view property type"),
            ("can_view_density_bar", "Can view density bar"),
            ("can_view_property_available", "Can view property available"),
            ("can_view_age_group", "Can view age group"),
            ("can_view_area_available", "Can view area available"),
            (
                "can_view_province_species_count",
                "Can view province species count"
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
            (
                "can_view_sampling_report",
                "Can view sampling report",
            ),
            (
                "can_view_province_report",
                "Can view province report",
            ),
            (
                "can_view_organisation_filter",
                "Can view organisation filter",
            ),
            (
                "can_view_property_filter",
                "Can view property filter",
            ),
            (
                "can_view_property_count_per_area_category",
                "Can view property count per area category",
            ),
            (
                ("can_view_property_count_per_"
                 "area_available_to_species_category"),
                ("Can view property count per "
                 "area available to species category"),
            ),
            (
                "can_view_property_count_per_population_density_category",
                "Can view property count per population density category",
            ),
            # Used in species report
            # Organisation Manager + Member should have this
            (
                "can_add_species_population_data",
                PERM_CAN_ADD_SPECIES_POPULATION_DATA
            ),
            (
                "can_edit_species_population_data",
                "Can edit species population data",
            ),
            # Used in trends tab
            (
                'can_view_properties_trends_data',
                'Can view properties trends data'
            ),
            # Used in report
            # Data consumer should have this
            (
                "can_view_report_as_data_consumer",
                "Can view report as data consumer"
            ),
            # Provincial data consumer should have this
            (
                "can_view_report_as_provincial_data_consumer",
                "Can view report as provincial data consumer"
            ),
            (
                "can_change_data_use_permissions",
                PERM_CAN_CHANGE_DATA_USE
            ),
        ]


@receiver(post_save, sender=Group)
def save_extended_group(sender, instance, created, **kwargs):
    """
    Handle ExtendedGroup creation and saving for the Group
    """
    extended_group, created = (
        ExtendedGroup.objects.get_or_create(group=instance)
    )

    if not created:
        instance.extended.save()
