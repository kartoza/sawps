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


class AnnualPopulationAbstract(models.Model):
    """"Annual Population model."""
    year = models.PositiveIntegerField()
    owned_species = models.ForeignKey(
        'species.OwnedSpecies', on_delete=models.CASCADE)
    total = models.IntegerField()
    adult_male = models.IntegerField(null=True, blank=True)
    adult_female = models.IntegerField(null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    juvenile_male = models.IntegerField(null=True, blank=True)
    juvenile_female = models.IntegerField(null=True, blank=True)
    area_covered = models.FloatField(null=False, default=0.0)
    sampling_effort = models.FloatField(null=False, default=0.0)
    group = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    survey_method = models.ForeignKey(
        'occurrence.SurveyMethod',
        on_delete=models.CASCADE,
        null=True
    )
    count_method = models.ForeignKey(
        'population_data.CountMethod',
        on_delete=models.CASCADE,
        null=True
    )
    sampling_size_unit = models.ForeignKey(
        'occurrence.SamplingSizeUnit',
        on_delete=models.CASCADE,
        null=True
    )
    certainty = models.ForeignKey(
        'population_data.Certainty',
        on_delete=models.CASCADE,
        null=True
    )
    open_close_system = models.ForeignKey(
        'population_data.OpenCloseSystem',
        on_delete=models.CASCADE,
        null=True
    )


    class Meta:
        abstract = True


class AnnualPopulation(AnnualPopulationAbstract):
    """Population count model."""
    sub_adult_total = models.IntegerField(null=True, blank=True)
    sub_adult_male = models.IntegerField(null=True, blank=True)
    sub_adult_female = models.IntegerField(null=True, blank=True)
    juvenile_total = models.IntegerField(null=True, blank=True)
    pride = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Annual Population'
        verbose_name_plural = 'Annual Populations'
        db_table = 'annual_population'
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'owned_species'],
                name='unique_population_count'),
            models.CheckConstraint(
                name=(
                    'Adult male and adult female must not '
                    'be greater than total'
                ),
                check=models.Q(total__gte=
                               models.F('adult_male') +
                               models.F('adult_female'))
            )
        ]


class AnnualPopulationPerActivity(AnnualPopulationAbstract):
    """Annual Population per activity model."""
    activity_type = models.ForeignKey('activity.ActivityType',
                                      on_delete=models.CASCADE)
    founder_population = models.BooleanField(null=True, blank=True)
    reintroduction_source = models.CharField(
        max_length=250, null=True, blank=True
    )
    permit_number = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Population count per activity'
        verbose_name_plural = 'Population count per activities'
        db_table = 'annual_population_per_activity'
        constraints = [models.UniqueConstraint(
            fields=['year', 'owned_species', 'activity_type'],
            name='unique_population_count_per_activity'
        )]


class Certainty(models.Model):
    """Certainty model"""
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
        unique=True
    )
    description = models.TextField(
        null=True, blank=True, help_text='Description')

    class Meta:
        verbose_name = 'Certainty'
        verbose_name_plural = 'Certainties'
        db_table = 'certainty'


class OpenCloseSystem(models.Model):
    """OpenCloseSystem model"""
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
        unique=True
    )

    class Meta:
        verbose_name = 'Open Close System'
        verbose_name_plural = 'Open Close System'
        db_table = 'open_close_system'

    def __str__(self) -> str:
        return self.name
