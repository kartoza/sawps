"""Model for Website Preferences."""
from django.db import models

from core.models.singleton import SingletonModel


class SitePreferences(SingletonModel):
    """Preference settings specifically for website.

    Preference contains
    - site_title
    - property_overlaps_threshold
    """

    site_title = models.CharField(
        max_length=512,
        default='SANBI'
    )

    # -----------------------------------------------
    # Property Overlaps Threshold for checking overlaps between properties
    # -----------------------------------------------
    property_overlaps_threshold = models.FloatField(
        null=True,
        blank=True,
        default=1,
        help_text=(
            'Threshold for checking overlaps between properties (in sqm).'
        )
    )

    @staticmethod  # noqa
    def preferences() -> "SitePreferences":
        """Load Site Preference."""
        return SitePreferences.load()

    def __str__(self):
        return 'Site Preference'
