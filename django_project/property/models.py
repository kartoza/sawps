from django.db import models


class PropertyType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class META:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'
        db_table = 'property_type'
