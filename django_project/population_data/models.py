from django.db import models


class CountMethod(models.Model):
    """count method model"""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'count method'
        verbose_name_plural = 'count methods'
        db_table = 'count_method'