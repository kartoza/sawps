from django.db import models

class dataUsePermission(models.Model):
    """data use permission model"""

    data_use_permissions = (('full public access','Full Public Access'), ('no public access','No Public Access'))
    name = models.CharField(
        unique=True, max_length=150, choices=data_use_permissions
    )
    description = models.TextField()

    class Meta:
        verbose_name = 'Data use permission'
        verbose_name_plural = 'Data use permissions'


class dataUsePermissionChange(models.Model):
    """data use permission change model"""

    date = models.DateField()
    # organization_id = models.ForeignKey(
    #     'stakeholder.Organization', on_delete=models.DO_NOTHING
    # )
    new_data_use_permission_id = models.ForeignKey(
        dataUsePermission, on_delete=models.CASCADE, related_name='new_data_use_permissions'
    )
    previous_data_use_permission_id = models.ForeignKey(
        dataUsePermission, on_delete=models.CASCADE, related_name='previous_data_use_permission'
    )
    user_id = models.ForeignKey(
        'stakeholder.UserProfile', on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Data use permission change'
        verbose_name_plural = 'Data use permission change'
