from django.db import models


class UserRoleType(models.Model):
    """user role type (Base users, admins ..etc.) model"""

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User role"
        verbose_name_plural = "User roles"
