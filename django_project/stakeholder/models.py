from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from property.models import Province


class UserRoleType(models.Model):
    """User role type (Base users, admins ..etc.) model."""

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User role'
        verbose_name_plural = 'User roles'
        db_table = 'user_role'


class LoginStatus(models.Model):
    """User login status model."""

    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Login status'
        verbose_name_plural = 'Login status'
        db_table = "login_status"


class UserTitle(models.Model):
    """User title model."""

    name = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        db_table = "user_title"


class UserLogin(models.Model):
    """User login model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_status = models.ForeignKey(
        LoginStatus,
        on_delete=models.DO_NOTHING
    )
    ip_address = models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User login'
        verbose_name_plural = 'User logins'
        db_table = "user_login"


class Organisation(models.Model):
    """Organisation model."""

    name = models.CharField(unique=True, max_length=250)
    data_use_permission = models.ForeignKey(
        'regulatory_permit.dataUsePermission',
        on_delete=models.DO_NOTHING
    )
    national = models.BooleanField(null=True, blank=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    use_of_data_by_sanbi_only = models.BooleanField(
        default=False
    )
    hosting_through_sanbi_platforms = models.BooleanField(
        default=False
    )
    allowing_sanbi_to_expose_data = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
        db_table = "organisation"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extend User model with one-to-one mapping."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        unique=True,
        related_name='user_profile'
    )
    title_id = models.ForeignKey(
        UserTitle,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None
    )
    cell_number = models.CharField(
        max_length=15,
        default='',
        null=True,
        blank=True
    )
    user_role_type_id = models.ForeignKey(
        UserRoleType,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None
    )
    picture = models.ImageField(
        upload_to='profile_pictures',
        null=True,
        blank=True
    )
    received_notif = models.BooleanField(default=False)
    current_organisation = models.ForeignKey(
        Organisation,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def picture_url(self):
        if self.picture.url:
            return '{media}/{url}'.format(
                    media=settings.MEDIA_ROOT,
                    url=self.picture,
            )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = "user_profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a user is created, also create a UserProfile
    """
    if (
        created and
        not UserProfile.objects.filter(user=instance).exists()
    ):
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile whenever a save event occurs
    """
    try:
        instance.user_profile.save()
    except AttributeError:
        UserProfile.objects.create(user=instance)


class OrganisationInvites(models.Model):
    """OrganisationInvites model to store all invites"""
    MEMBER = 'Member'
    MANAGER = 'Manager'
    ASSIGNED_CHOICES = [
        (MEMBER, 'Member'),
        (MANAGER, 'Manager'),
    ]
    email = models.CharField(max_length=200, null=True, blank=True)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    joined = models.BooleanField(
        default=False,
        null=True, blank=True
    )
    user_role = models.ForeignKey(
        UserRoleType,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None
    )
    assigned_as = models.CharField(
        max_length=50,
        choices=ASSIGNED_CHOICES,
        default=MEMBER
    )

    class Meta:
        verbose_name = 'OrganisationInvites'
        verbose_name_plural = 'OrganisationInvites'
        db_table = "OrganisationInvites"

    def __str__(self):
        return str(self.email)


class Reminders(models.Model):
    """Reminders model to store all reminders"""
    ACTIVE = 'Active'
    DRAFT = 'Draft'
    PASSED = 'Passed'
    ASSIGNED_CHOICES = [
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft'),
        (PASSED, 'Passed')
    ]
    PERSONAL = 'Personal'
    EVERYONE = 'Everyone'
    TYPES = [
        (PERSONAL, 'Personal'),
        (EVERYONE, 'Everyone')
    ]
    title = models.CharField(
        max_length=200,
        null=True, blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(
        max_length=50,
        choices=TYPES,
        default=PERSONAL
    )
    reminder = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=ASSIGNED_CHOICES,
        default=ACTIVE
    )
    email_sent = models.BooleanField(default=False)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(
        max_length=120,
        default='Africa/Johannesburg'
    )

    class Meta:
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'
        db_table = "Reminders"

    def __str__(self):
        return str(self.title)


class OrganisationPersonnel(models.Model):
    """Organisation personnel abstract model."""
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OrganisationRepresentative(OrganisationPersonnel):
    """Organisation representative model."""
    class Meta:
        verbose_name = 'Organisation representative'
        verbose_name_plural = 'Organisation representatives'
        db_table = 'organisation_representative'


class OrganisationUser(OrganisationPersonnel):
    """Organisation user model."""
    class Meta:
        verbose_name = 'Organisation user'
        verbose_name_plural = 'Organisation users'
        db_table = 'organisation_user'
