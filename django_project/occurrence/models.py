from django.db import models


class OrganismQuantityType(models.Model):
    """Organism quantity type model."""
    class Meta:
        verbose_name = "organism_quantity_type"
        verbose_name_plural = "organism_quantity_type"
        db_table = "organism_quantity_type"


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
