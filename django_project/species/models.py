from django.db import models
from django.contrib.auth.models import User


class ManagementStatus(models.Model):
    """Management status model."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Management Status"
        verbose_name_plural = "Management Status"
        db_table = 'management_status'


class TaxonRank(models.Model):
    """Taxon rank model."""

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Taxon Rank'
        verbose_name_plural = 'Taxon Ranks'
        db_table = 'taxon_rank'


class Taxon(models.Model):
    """Taxon model."""
    scientific_name = models.CharField(max_length=250, unique=True)
    common_name_varbatim = models.CharField(max_length=250, null=True, blank=True)
    colour_variant = models.BooleanField()
    infraspecific_epithet = models.CharField(max_length=250, unique=True, null=True, blank=True)
    taxon_rank = models.ForeignKey('species.TaxonRank', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.scientific_name
    
    class Meta:
        verbose_name = 'Taxon'
        verbose_name_plural = 'Taxa'
        db_table = 'taxon'


class OwnedSpecies(models.Model):
    """Owned species mdoel."""
    management_status = models.ForeignKey('species.ManagementStatus', on_delete=models.CASCADE)
    nature_of_population = models.ForeignKey('population_data.NatureOfPopulation', on_delete=models.CASCADE)
    count_method = models.ForeignKey('population_data.CountMethod', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taxon = models.ForeignKey('species.Taxon', on_delete=models.CASCADE)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)

    def __str__(self):
                return f'Owned species#{self.id}'

    class Meta:
        verbose_name = 'Owned Species'
        verbose_name_plural = 'Owned Species'
        db_table = 'owned_species'
