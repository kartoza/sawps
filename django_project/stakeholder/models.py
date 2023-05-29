from django.db import models

# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserTitle(models.Model):
    """user title model"""

    user_titles = [
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),
        ('miss', 'Miss'),
        ('dr', 'Dr'),
    ]
    name = models.CharField(unique=True, max_length=10, choices=user_titles)

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class UserRoleType(models.Model):
    """user role type (Base users, admins ..etc.) model"""

    user_roles = [
        ('base user', 'Base User'),
        ('data contributor', 'Data Contributor'),
        ('decision maker', 'Decision maker'),
        ('super user', 'Super user'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(unique=True, max_length=50, choices=user_roles)
    description = models.TextField()

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'


class UserProfile(models.Model):
    """extend User Model, using one-to-one mapping temporarly"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title_id = models.ForeignKey(UserTitle, on_delete=models.DO_NOTHING)
    cell_number = models.IntegerField()
    user_role_type_id = models.ForeignKey(
        UserRoleType, on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class LoginStatus(models.Model):
    """user login status model"""

    status = [('logged in', 'Logged in'), ('logged out', 'Logged out')]
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
        'regulatory_permit.dataUsePermission', on_delete=models.DO_NOTHING
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
