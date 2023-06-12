from django.contrib.gis.db import models
from django.contrib.auth.models import User

class OrganismQuantityType(models.Model):
    """Organism quantity type model."""

    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'organism_quantity_type'
        verbose_name_plural = 'organism_quantity_type'
        db_table = 'organism_quantity_type'


class SurveyMethod(models.Model):
    """Survey method model."""

    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Survey method'
        verbose_name_plural = 'Survey methods'
        db_table = 'survey_method'


class OccurrenceStatus(models.Model):
    """Occurrence status model."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Occurrence status'
        verbose_name_plural = 'Occurrence statuses'
        db_table = 'occurrence_status'


class BasisOfRecord(models.Model):
    """Basis of record model."""

    name = models.CharField(max_length=150, unique=True)
    sort_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Basis of record'
        verbose_name_plural = 'Basis of records'
        db_table = 'basis_of_record'


class SamplingSizeUnit(models.Model):
    """Sampling size unit model."""

    unit = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = 'Sampling size unit'
        verbose_name_plural = 'Sampling size units'
        db_table = 'sampling_size_unit'


class Occurrence(models.Model):
    """Occurrence model."""
    individual_count = models.IntegerField()
    organism_quantity = models.IntegerField()
    sampling_size_value = models.FloatField()
    datetime = models.DateTimeField(null=True, blank=True)
    owner_institution_code = models.CharField(max_length=250)
    coordinates_uncertainty_m = models.IntegerField()
    geometry = models.PointField(srid=4326, null=True, blank=True)
    taxon = models.ForeignKey('species.Taxon', on_delete=models.CASCADE)
    basis_of_record = models.ForeignKey(
        BasisOfRecord, on_delete=models.CASCADE
    )
    ogranism_quantity_type = models.ForeignKey(
        OrganismQuantityType, on_delete=models.CASCADE
    )
    occurrence_status = models.ForeignKey(
        OccurrenceStatus, on_delete=models.CASCADE
    )
    sampling_size_unit = models.ForeignKey(
        SamplingSizeUnit, on_delete=models.CASCADE
    )
    survey_method = models.ForeignKey(
        SurveyMethod, on_delete=models.CASCADE
    )
    organisation = models.ForeignKey(
        'stakeholder.Organisation', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Occurrence'
        verbose_name_plural = 'Occurrences'
        db_table = 'occurrence'