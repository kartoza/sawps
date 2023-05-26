from django.db import models
from django.contrib.auth.models import User
import regulatory_permits.models as regulatoryPermitsModels


class Title(models.Model):
    """title model"""

    titles = ('Mr', 'Mrs', 'Ms', 'Miss', 'Dr')
    name = models.CharField(unique=True, max_length=10, choices=titles)

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class UserRoleType(models.Model):
    """user role type model"""

    user_roles = (
        'Base User',
        'Data Contributor',
        'Decision maker',
        'Super user',
        'Admin',
    )
    name = models.CharField(unique=True, max_length=50, choices=user_roles)
    description = models.TextField()

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'


class UserProfile(User):
    """extend User Model, using one-to-one mapping temporarly"""

    title_id = models.ForeignKey(Title, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    date_joined = models.DateField()
    email = models.EmailField(unique=True)
    cell_number = models.IntegerField()
    is_active = models.BooleanField(null=True, blank=True)
    user_role_type_id = models.ForeignKey(
        UserRoleType, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class LoginStatus(models.Model):
    """user login model"""

    status = ('Logged in', 'Logged out')
    name = models.CharField(unique=True, max_length=50, choices=status)

    class Meta:
        verbose_name = 'Login status'
        verbose_name_plural = 'Login status'


class UserLogin(models.Model):
    """user login model"""

    datetime = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=15)
    login_status_id = models.ForeignKey(
        LoginStatus, on_delete=models.DO_NOTHING
    )
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User login'
        verbose_name_plural = 'Users login'


class Organization(models.Model):
    """organization model"""

    name = models.CharField(unique=True, max_length=250)
    data_use_permission_id = models.ForeignKey(
        regulatoryPermitsModels.dataUsePermission, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class OrganizationRepresentatives(models.Model):
    """organization representatives model"""

    organization_id = models.ForeignKey(
        Organization, on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Organization representative'
        verbose_name_plural = 'Organization representatives'


class OrganizationUser(models.Model):
    """organization user model"""

    organization_id = models.ForeignKey(
        Organization, on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Organization user'
        verbose_name_plural = 'Organization users'
