from django.db import models


class PopulationCountAbstract(models.Model):
    """population count abstract model"""

    year = models.DateField(primary_key=True)
    owned_species_id = models.ManyToManyField('species.OwnedSpecies')
    total = models.IntegerField()
    adult_males = models.IntegerField(null=True, blank=True)
    adult_females = models.IntegerField(null=True, blank=True)
    pride = models.IntegerField(null=True, blank=True)
    month_id = models.ForeignKey('species.Month', on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class CountMethod(models.Model):
    """count method model"""

    count_methods_list = [
        ('distance sampling', 'Distance sampling'),
        ('point sampling', 'Point sampling'),
        ('quadrant sampling', 'Quadrant sampling'),
        ('transect sampling', 'Transect sampling'),
        ('line sampling', 'Line sampling'),
        ('belt sampling', 'Belt sampling'),
        ('stratified sampling', 'Stratified sampling'),
        ('systematic sampling', 'Systematic sampling'),
        ('opportunistic sampling', 'Opportunistic sampling'),
        ('mark capture', 'Mark capture'),
    ]
    name = models.CharField(
        unique=True, max_length=200, choices=count_methods_list
    )

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

    activity_type_id = models.ManyToManyField('activity.ActivityType')
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

    nature_of_population_list = [
        ('free range', 'Free Range'),
        ('enclosure', 'Enclosure'),
    ]
    name = models.CharField(
        max_length=150, unique=True, choices=nature_of_population_list
    )
    extensive = models.BooleanField()

    class Meta:
        verbose_name = 'Nature of population'
        verbose_name_plural = 'Nature of population'
