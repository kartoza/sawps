from django.db import models


class dataUsePermission(models.Model):
    """data use permission model"""

    name = models.CharField(unique=True, max_length=150)
    description = models.TextField()

    class Meta:
        verbose_name = 'Data use permission'
        verbose_name_plural = 'Data use permissions'


class dataUsePermissionChange(models.Model):
    """data use permission change model"""

    date = models.DateField()
    organization = models.ForeignKey(
        'stakeholder.Organization', on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        'stakeholder.UserProfile', on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Data use permission change'
        verbose_name_plural = 'Data use permission change'
