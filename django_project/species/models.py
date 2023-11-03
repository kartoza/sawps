"""Species models.
"""
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator


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
    icon = models.ImageField(
        upload_to="taxon_icons",
        null=True, blank=True
    )
    graph_icon = models.FileField(
        upload_to="taxon_graph_icons",
        null=True, blank=True,
        validators=[FileExtensionValidator(['svg'])],
        help_text=(
            'Use SVG file with black fill and transparent background. '
            'It will be used as species icon in graph/charts.'
        )
    )
    topper_icon = models.FileField(
        upload_to="taxon_topper_icons",
        null=True, blank=True,
        validators=[FileExtensionValidator(['svg'])],
        help_text=(
            'Will be generated automatically from graph_icon to be used in '
            'Report and Charts topper. Pleae re-upload graph_icon to '
            'regenerate topper_icon.'
        )
    )

    def __str__(self):
        return self.scientific_name

    class Meta:
        verbose_name = "Taxon"
        verbose_name_plural = "Taxa"
        db_table = "taxon"

    def save(self, *args, **kwargs):
        svg_content = self.graph_icon.read()
        svg_content = svg_content.replace(b'fill="#000000"', b'fill="#75B37A"')
        svg_content = svg_content.replace(b'fill="black"', b'fill="#75B37A"')
        topper_icon = ContentFile(svg_content, name=f"{self.scientific_name}-topper.svg")
        self.topper_icon = topper_icon
        return super().save(*args, **kwargs)


class OwnedSpecies(models.Model):
    """Owned species mdoel."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taxon = models.ForeignKey("species.Taxon", on_delete=models.CASCADE)
    property = models.ForeignKey("property.Property", on_delete=models.CASCADE)
    area_available_to_species = models.FloatField(default=0.0)

    def __str__(self):
        return self.property.name

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
