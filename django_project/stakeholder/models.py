from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserTitle(models.Model):
    """user title model"""

    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class UserRoleType(models.Model):
    """user role type (Base users, admins ..etc.) model"""

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'


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


class LoginStatus(models.Model):
    """user login status model"""

    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Login status'
        verbose_name_plural = 'Login status'


class UserLogin(models.Model):
    """user login model"""

    datetime = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=15)
    login_status_id = models.ForeignKey(
        LoginStatus, on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.user.username} - {self.datetime}'

    class Meta:
        verbose_name = 'User login'
        verbose_name_plural = 'Users login'


class Organization(models.Model):
    """organization model"""

    name = models.CharField(unique=True, max_length=250)
    data_use_permission = models.ForeignKey(
        'regulatory_permit.dataUsePermission', on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class AbstractOrganizationPersonnel(models.Model):
    """Abstact organization personnel model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OrganizationRepresentatives(AbstractOrganizationPersonnel):
    """organization representatives model"""

    class Meta:
        verbose_name = 'Organization representative'
        verbose_name_plural = 'Organization representatives'


class OrganizationUser(AbstractOrganizationPersonnel):
    """organization user model"""

    class Meta:
        verbose_name = 'Organization user'
        verbose_name_plural = 'Organization users'
