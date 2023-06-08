from django.db import models
from django.contrib.auth.models import User


class UserRoleType(models.Model):
    """user role type (Base users, admins ..etc.) model"""

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'
        db_table = 'user_role'


class LoginStatus(models.Model):
    """user login status model"""

    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

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


class UserProfile(models.Model):
    """extend User model with one-to-one mapping"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    title_id = models.ForeignKey(UserTitle, on_delete=models.DO_NOTHING)
    cell_number = models.IntegerField()
    user_role_type_id = models.ForeignKey(
        UserRoleType, on_delete=models.DO_NOTHING
    )

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = "user_profile"