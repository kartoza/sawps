from django.contrib.gis.db import models
import species.models as species_models
import stakeholder.models as stackHolderModels


class OccurrenceStatus(models.Model):
    """occurrence status model"""

    status = ('Absent', 'Present')
    name = models.CharField(unique=True, choices=status, max_length=50)

    class Meta:
        verbose_name = 'Occurrence status'
        verbose_name_plural = 'Occurrences status'


class BasisOfRecord(models.Model):
    """basis of records model"""

    choices = (
        'Preserved Specimen',
        'Fossil Specimen',
        'Living Specimen',
        'Human Observation',
        'Machine Observation',
    )
    name = models.CharField(max_length=100, choices=choices, unique=True)
    sort_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'Basis of record'
        verbose_name_plural = 'Bases of records'


class SamplingSizeUnit(models.Model):
    """sample size unit model"""

    units = ('m', 'cm', 'km')
    unit = models.CharField(max_length=2, choices=units, unique=True)

    class Meta:
        verbose_name = 'Sampling size unit'
        verbose_name_plural = 'Sampling size units'


class OrganismQuantityType(models.Model):
    """organism quantity type model"""

    organism_quantity_types_list = (
        'Individual',
        'Biomass',
        'Braun Blanquet Scale',
    )
    name = models.CharField(
        max_length=200, unique=True, choices=organism_quantity_types_list
    )
    sort_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'Organism quantity type'
        verbose_name_plural = 'Organism quantity types'


class SurveyMethod(models.Model):
    """survey method model"""

    survey_methods_list = (
        'Point count',
        'Transect survey - foot',
        'Transect survey - aerial',
        'Transect survey - drive',
        'Block survey - foot',
        'Block survey - aerial',
        'Quadrant survey',
        'Camera survey',
        'Pritfall trapping',
        'Aquatic survey',
        'Total count (census)',
        'Unknown',
        'Estimate',
    )
    name = models.CharField(
        unique=True, max_length=250, choices=survey_methods_list
    )
    sort_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'Survey method'
        verbose_name_plural = 'survey methods'


class Occurrence(models.Model):
    """occurrence model"""

    individual_count = models.IntegerField()
    organism_quantity = models.IntegerField()
    sampling_size_value = models.FloatField()
    datetime = models.DateTimeField(null=True, blank=True)
    owner_institution_code = models.CharField(max_length=250)
    coordinates_uncertainty_m = models.IntegerField()
    geometry = models.PointField(srid=4326)
    taxon_id = models.ForeignKey(
        species_models.Taxon, on_delete=models.DO_NOTHING
    )
    basis_of_record_id = models.ForeignKey(
        BasisOfRecord, on_delete=models.DO_NOTHING
    )
    ogranism_quantity_type = models.ForeignKey(
        OrganismQuantityType, on_delete=models.DO_NOTHING
    )
    occurrence_status_id = models.ForeignKey(
        OccurrenceStatus, on_delete=models.DO_NOTHING
    )
    sampling_size_unit_id = models.ForeignKey(
        SamplingSizeUnit, on_delete=models.DO_NOTHING
    )
    survey_method_id = models.ForeignKey(
        SurveyMethod, on_delete=models.DO_NOTHING
    )
    organisation_id = models.ForeignKey(
        stackHolderModels.Organization, on_delete=models.DO_NOTHING
    )
    user_id = models.ForeignKey(
        stackHolderModels.UserProfile, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Occurrence'
        verbose_name_plural = 'Occurrences'
