from django.contrib.auth.models import User
from django.db import models


class TaxonRank(models.Model):
    """Taxon rank model."""

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taxon Rank"
        verbose_name_plural = "Taxon Ranks"
        db_table = "taxon_rank"


class Taxon(models.Model):
    """Taxon model."""

    scientific_name = models.CharField(max_length=250, unique=True)
    common_name_varbatim = models.CharField(
        max_length=250,
        null=True, blank=True)
    colour_variant = models.BooleanField(null=True, blank=True)
    infraspecific_epithet = models.CharField(
        max_length=250, unique=True, null=True, blank=True
    )
    taxon_rank = models.ForeignKey(
        "species.TaxonRank",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)
    show_on_front_page = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    front_page_order = models.PositiveIntegerField(
        verbose_name="Front page order", null=False, blank=True, default=0
    )
    colour = models.CharField(max_length=20, null=True, blank=True)
    icon = models.ImageField(upload_to="taxon_icons", null=True, blank=True)

    def __str__(self):
        return self.scientific_name

    class Meta:
        verbose_name = "Taxon"
        verbose_name_plural = "Taxa"
        db_table = "taxon"


class OwnedSpecies(models.Model):
    """Owned species mdoel."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taxon = models.ForeignKey("species.Taxon", on_delete=models.CASCADE)
    property = models.ForeignKey("property.Property", on_delete=models.CASCADE)
    area_available_to_species = models.FloatField(default=0.0)

    def __str__(self):
        return f"Owned species#{self.id}"

    class Meta:
        verbose_name = "Owned Species"
        verbose_name_plural = "Owned Species"
        db_table = "owned_species"


class TaxonSurveyMethod(models.Model):
    """taxon survey methods"""

    taxon = models.ForeignKey("species.Taxon", on_delete=models.CASCADE)
    survey_method = models.ForeignKey(
        "occurrence.SurveyMethod", on_delete=models.CASCADE
    )
