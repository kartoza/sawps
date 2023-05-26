from django.db import models
import stakeholder.models as stackHolderModels


class dataUsePermission(models.Model):
    """data use permission model"""

    data_use_permissions = ('Full Public Access', 'No Public Access')
    name = models.CharField(
        unique=True, max_length=150, choices=data_use_permissions
    )
    description = models.TextField()

    class Meta:
        verbose_name = 'Data use permission'
        verbose_name_plural = 'Data use permissions'


class dataUsePermissionChange(models.Model):
    """data use permission change model"""

    data = models.DateField()
    organization_id = models.ForeignKey(
        stackHolderModels.Organization, on_delete=models.DO_NOTHING
    )
    new_data_use_permission_id = models.ForeignKey(
        dataUsePermission, on_delete=models.CASCADE
    )
    previous_data_use_permission_id = models.ForeignKey(
        dataUsePermission, on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        stackHolderModels.UserProfile, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Data use permission change'
        verbose_name_plural = 'Data use permission change'
