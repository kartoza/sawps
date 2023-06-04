from django.db import models

class NatureOfPopulation(models.Model):
    """
    nature of the population model.
    """
    name = models.CharField(max_length=255, unique=True)
    extensive = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nature of Population'
        verbose_name_plural = 'Nature of Population'
        db_table = 'nature_of_population'