from django.db import models


class DataUsePermission(models.Model):
    """data use permission model"""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_use_permission'
        verbose_name = 'data use permission'
        verbose_name_plural = 'data use permissions'
