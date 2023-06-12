from django.db import models


class CountMethod(models.Model):
    """Count method model."""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'count method'
        verbose_name_plural = 'count methods'
        db_table = 'count_method'


class Month(models.Model):
    """Month model."""

    name = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'month'
        verbose_name_plural = 'months'
        db_table = 'month'


class NatureOfPopulation(models.Model):
    """Nature of the population model."""

    name = models.CharField(max_length=255, unique=True)
    extensive = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nature of Population'
        verbose_name_plural = 'Nature of Population'
        db_table = 'nature_of_population'


class PopulationCountAbstract(models.Model):
    """"Populaiton count abstract model."""
    year = models.DateField()
    owned_species = models.ForeignKey('species.OwnedSpecies', on_delete=models.CASCADE)
    total = models.IntegerField()
    adult_male = models.IntegerField(null=True, blank=True)
    adult_female = models.IntegerField(null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    juvenile_male = models.IntegerField(null=True, blank=True)
    juvenile_female = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class PopulationCount(PopulationCountAbstract):
    """Population count model."""
    sub_adult_total = models.IntegerField(null=True, blank=True)
    sub_adult_male = models.IntegerField(null=True, blank=True)
    sub_adult_female = models.IntegerField(null=True, blank=True)
    juvenile_total = models.IntegerField(null=True, blank=True)
    pride = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Population count'
        verbose_name = 'Population counts'
        db_table = 'population_count'
        constraints = [models.UniqueConstraint(
            fields=['year', 'owned_species'],name='unique_population_count'
        )]
        unique_together = ('year', 'owned_species')

class PopulationCountPerActivity(PopulationCountAbstract):
    """Population count per activity model."""
    activity_type = models.ForeignKey('activity.ActivityType', on_delete=models.CASCADE)
    founder_population = models.BooleanField(null=True, blank=True)
    reintroduction_source = models.CharField(
        max_length=250, null=True, blank=True
    )
    permit_number = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Population count per activity'
        verbose_name = 'Population count per activities'
        db_table = 'population_count_per_activity'
        constraints = [models.UniqueConstraint(
            fields=['year', 'owned_species', 'activity_type'],name='unique_population_count_per_activity'
        )]
