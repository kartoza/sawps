from django.db import models


class UserRoleType(models.Model):
    """user role type (Base users, admins ..etc.) model"""

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'
        db_table = 'user_role'


class LoginStatus(models.Model):
    """user login status model"""

    name = models.CharField(unique=True, max_length=20)

    class Meta:
        verbose_name = 'Login status'
        verbose_name_plural = 'Login status'
        db_table = "login_status"


class UserTitle(models.Model):
    """user title model"""

    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        db_table = "user_title"