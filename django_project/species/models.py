from django.db import models


class ManagementStatus(models.Model):
    """management status model"""

    management_status = [
        ('self sustaining', 'Self-sustaining'),
        ('managed', 'Managed'),
    ]
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
    parent_id = models.ForeignKey('self', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Taxon'
        verbose_name_plural = 'Taxa'


class OwnedSpecies(models.Model):
    """owned species model"""

    management_status_id = models.ForeignKey(
        ManagementStatus, on_delete=models.DO_NOTHING
    )
    nature_of_population_id = models.ForeignKey(
        'population_data.NatureOfPopulation', on_delete=models.DO_NOTHING
    )
    count_method_id = models.ForeignKey(
        'population_data.CountMethod', on_delete=models.DO_NOTHING
    )
    user_id = models.ForeignKey(
        'stakeholder.UserProfile', on_delete=models.DO_NOTHING
    )
    taxon_id = models.ForeignKey(Taxon, on_delete=models.DO_NOTHING)
    property_id = models.ForeignKey(
        'property.Property', on_delete=models.DO_NOTHING
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
