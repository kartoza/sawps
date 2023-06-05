from django.db import models


class Month(models.Model):
    """month model"""

    name = models.CharField(max_length=100, unique=True)
    sorid = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'month'
        verbose_name_plural = 'months'
        db_table = 'month'