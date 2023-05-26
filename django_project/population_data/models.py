from django.db import models
import species.models as speciesModels
import Activity.models as ActivityModels


class PopulationCountAbstract(models.Model):
    """population count abstract model"""

    year = models.DateField(primary_key=True)
    owned_species_id = models.ManyToManyField(
        speciesModels.OwnedSpecies, on_delete=models.DO_NOTHING
    )
    total = models.IntegerField()
    adult_males = models.IntegerField(null=True, blank=True)
    adult_females = models.IntegerField(null=True, blank=True)
    pride = models.IntegerField(null=True, blank=True)
    month_id = models.ForeignKey(
        speciesModels.Month, on_delete=models.DO_NOTHING
    )

    class Meta:
        abstract = True


class CountMethod(models.Model):
    """count method model"""

    count_methods_list = (
        'Distance sampling',
        'Point sampling',
        'Quadrant sampling',
        'Transect sampling',
        'Line sampling',
        'Belt sampling',
        'Stratified sampling',
        'Systematic sampling',
        'Opportunistic sampling',
        'Mark capture',
    )
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        verbose_name = 'Count method'
        verbose_name_plural = 'Count methods'


class PopulationCount(PopulationCountAbstract):
    """population count model"""

    sub_adult_total = models.IntegerField(null=True, blank=True)
    sub_adult_male = models.IntegerField(null=True, blank=True)
    sub_adult_female = models.IntegerField(null=True, blank=True)
    juvenile_total = models.IntegerField(null=True, blank=True)
    juvenile_male = models.IntegerField(null=True, blank=True)
    juvenile_female = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Population count'
        verbose_name = 'Population counts'


class PopulationCountPerActivity(PopulationCountAbstract):
    """population count per activity model"""

    activity_type_id = models.ManyToManyField(
        ActivityModels.ActivityType, on_delete=models.DO_NOTHING
    )
    juveniles_males = models.IntegerField(null=True, blank=True)
    juveniles_females = models.IntegerField(null=True, blank=True)
    founder_population = models.BooleanField(null=True, blank=True)
    reintroduction_source = models.CharField(
        max_length=250, null=True, blank=True
    )
    permit_number = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Population count per activity'
        verbose_name = 'Population count per activities'


class NatureOfPopulation(models.Model):
    """nature of population model"""

    nature_of_population_list = ('Free Range', 'Enclosure')
    name = models.CharField(
        max_length=150, unique=True, choices=nature_of_population_list
    )
    extensive = models.BooleanField()

    class Meta:
        verbose_name = 'Nature of population'
        verbose_name_plural = 'Nature of population'
