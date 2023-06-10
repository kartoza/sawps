from django.db import models
from django.contrib.auth.models import User

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


class DataUsePermissionChange(models.Model):
    """Datause permission change model."""
    
    date = models.DateField()
    organisation = models.ForeignKey('stakeholder.Organisation', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.change_type

    class Meta:
        verbose_name = 'data use permission change'
        verbose_name_plural = 'data use permission changes'
        db_table = 'data_use_permission_change'
