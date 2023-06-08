from django.db import models


class Month(models.Model):
    """Month model."""

    name = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField(unique=True)

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

