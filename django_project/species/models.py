from django.db import models

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
