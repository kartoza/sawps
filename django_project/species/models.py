from django.db import models
import property.models as properties
import population_data.models as populationModels


class ManagementStatus(models.Model):
    """management status model"""

    management_status = ('Self-sustaining', 'Managed')
    name = models.CharField(
        unique=True, max_length=50, choices=management_status
    )

    class Meta:
        verbose_name = 'Management status'
        verbose_name_plural = 'Management status'


class TaxonRank(models.Model):
    """taxon rank model"""

    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Taxon rank'
        verbose_name_plural = 'Taxon ranks'


class Taxon(models.Model):
    """taxon model"""

    scientific_name = models.CharField(unique=True, max_length=250)
    common_name_varbatim = models.CharField(
        null=True, blank=True, max_length=250
    )
    colour_variant = models.BooleanField()
    infraspecific_epithet = models.CharField(
        unique=True, max_length=250, null=True, blank=True
    )
    taxon_rank_id = models.ForeignKey(TaxonRank, on_delete=models.DO_NOTHING)
    parent_id = models.ForeignKey('self')

    class Meta:
        verbose_name = 'Taxon'
        verbose_name_plural = 'Taxa'


class OwnedSpecies(models.Model):
    """owned species model"""

    management_status_id = models.ForeignKey(
        ManagementStatus, on_delete=models.DO_NOTHING
    )
    nature_of_population_id = models.ForeignKey(
        populationModels.NatureOfPopulation, on_delete=models.DO_NOTHING
    )
    count_method_id = models.ForeignKey(
        populationModels.CountMethod, on_delete=models.DO_NOTHING
    )
    user_id = models.ForeignKey(on_delete=models.DO_NOTHING)
    taxon_id = models.ForeignKey(Taxon, on_delete=models.DO_NOTHING)
    property_id = models.ForeignKey(
        properties.Property, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Owned species'
        verbose_name_plural = 'Owned species'


class Month(models.Model):
    """month model"""

    name = models.CharField(unique=True, max_length=250)
    sort_order = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'Month'
        verbose_name_plural = 'Months'
