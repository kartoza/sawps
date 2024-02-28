import uuid

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from property.models import Province
from stakeholder.utils import (
    add_user_to_org_member,
    add_user_to_org_manager,
    remove_user_from_org_member,
    remove_user_from_org_manager,
    notify_user_becomes_manager
)

MEMBER = 'Member'
MANAGER = 'Manager'


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
        on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return self.user.username
        except User.DoesNotExist:
            return str(self.id)

    class Meta:
        verbose_name = 'User login'
        verbose_name_plural = 'User logins'
        db_table = "user_login"


class Organisation(models.Model):
    """Organisation model."""

    name = models.CharField(unique=True, max_length=250)
    short_code = models.CharField(
        max_length=50,
        null=False,
        blank=True
    )
    national = models.BooleanField(null=True, blank=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
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

    def get_short_code(
        self,
        with_digit: bool = True
    ) -> str:
        from stakeholder.utils import get_organisation_short_code

        province_name = self.province.name if self.province else ''
        organisation_name = self.name
        return get_organisation_short_code(
            province_name=province_name,
            organisation_name=organisation_name,
            with_digit=with_digit,
            OrganisationModel=Organisation
        )


@receiver(pre_save, sender=Organisation)
def organisation_pre_save(
    sender, instance: Organisation, *args, **kwargs
):
    from stakeholder.utils import get_organisation_short_code

    if instance.id:
        old_org: Organisation = Organisation.objects.get(id=instance.id)
        is_name_changed = old_org.name != instance.name
        is_province_changed = old_org.province != instance.province
        if any([is_province_changed, is_name_changed]):
            instance.short_code = get_organisation_short_code(
                province_name=(
                    instance.province.name if instance.province else ''
                ),
                organisation_name=instance.name
            )
            instance.skip_post_save = False
    else:
        instance.short_code = instance.get_short_code()


@receiver(post_save, sender=Organisation)
def organisation_post_save(
    sender, instance: Organisation, created, *args, **kwargs
):
    from stakeholder.tasks import update_property_short_code

    if not created and not getattr(instance, 'skip_post_save', True):
        update_property_short_code.delay(instance.id)


class UserProfile(models.Model):
    """Extend User model with one-to-one mapping."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        unique=True,
        related_name='user_profile'
    )
    title_id = models.ForeignKey(
        UserTitle,
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
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
        try:
            return self.user.username
        except User.DoesNotExist:
            return str(self.id)

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
    if UserProfile.objects.filter(
        user=instance
    ).exists():
        instance.user_profile.save()
    else:
        UserProfile.objects.create(user=instance)


class OrganisationInvites(models.Model):
    """OrganisationInvites model to store all invites"""
    ASSIGNED_CHOICES = [
        (MEMBER, 'Member'),
        (MANAGER, 'Manager'),
    ]
    email = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    joined = models.BooleanField(
        default=False,
        null=True, blank=True
    )
    user_role = models.ForeignKey(
        UserRoleType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    assigned_as = models.CharField(
        max_length=50,
        choices=ASSIGNED_CHOICES,
        default=MEMBER
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        null=False,
        blank=True
    )

    class Meta:
        verbose_name = 'Organisation invite'
        verbose_name_plural = 'Organisation invites'
        db_table = "OrganisationInvites"
        permissions = [
            ("can_invite_people_to_organisation",
             "Can invite people to organisation"),
        ]

    def __str__(self):
        return str(self.email)

    def get_invitee(self):
        user = self.user
        if not user:
            user = User.objects.filter(email=self.email).first()
        return user


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
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
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
        verbose_name = 'Organisation manager'
        verbose_name_plural = 'Organisation managers'
        db_table = 'organisation_representative'


class OrganisationUser(OrganisationPersonnel):
    """Organisation user model."""
    class Meta:
        verbose_name = 'Organisation member'
        verbose_name_plural = 'Organisation members'
        db_table = 'organisation_user'


@receiver(post_save, sender=OrganisationUser)
def post_create_organisation_user(
    sender,
    instance: OrganisationUser,
    created,
    **kwargs
):
    """
    Handle OrganisationUser creation by
    automatically add them to Organisation Member group.
    """
    add_user_to_org_member(instance, OrganisationInvites, Group)


@receiver(post_delete, sender=OrganisationUser)
def post_delete_organisation_user(
    sender,
    instance: OrganisationUser,
    *args,
    **kwargs
):
    """
    Handle OrganisationUser deletion by removing them
    from Data contributor and Organisation Member group, if they are no longer
    part of any organisation.
    """
    remove_user_from_org_member(instance)
    # when user is removed from organisation
    # also remove it from current_organisation in UserProfile
    profile = UserProfile.objects.filter(
        user=instance.user,
        current_organisation=instance.organisation
    ).first()
    if profile:
        profile.current_organisation = None
        profile.save(update_fields=['current_organisation'])
    # when user is removed, ensure that manager is removed as well
    OrganisationRepresentative.objects.filter(
        user=instance.user,
        organisation=instance.organisation
    ).delete()
    # ensure invite record is removed
    OrganisationInvites.objects.filter(
        Q(email=instance.user.email) | Q(user=instance.user),
        organisation=instance.organisation
    ).delete()


@receiver(post_save, sender=OrganisationRepresentative)
def post_create_organisation_representative(
    sender,
    instance: OrganisationRepresentative,
    created,
    **kwargs
):
    """
    Handle OrganisationRepresentative creation by
    automatically add them to Organisation Manager group.
    """
    add_user_to_org_manager(instance, Group)
    # check if user becomes manager from member
    is_made_manager = False
    if created:
        organisation_user = OrganisationUser.objects.filter(
            user=instance.user,
            organisation=instance.organisation
        ).first()
        member_invite = OrganisationInvites.objects.filter(
            user=instance.user,
            joined=True
        ).first()
        if organisation_user is None:
            # case when representative is created in admin site
            # create organisation user
            OrganisationUser.objects.create(
                user=instance.user,
                organisation=instance.organisation
            )
            is_made_manager = True
        elif member_invite:
            # check if previously has been invited as member
            is_made_manager = member_invite.assigned_as == MEMBER
        else:
            # this case could be the member is added through admin site
            is_made_manager = True
    if is_made_manager:
        notify_user_becomes_manager(instance)


@receiver(post_delete, sender=OrganisationRepresentative)
def post_delete_organisation_representative(
    sender,
    instance: OrganisationRepresentative,
    *args,
    **kwargs
):
    """
    Handle OrganisationRepresentative deletion by removing them
    from Data contributor and Organisation Manager group, if they are no longer
    part of any organisation.
    """
    remove_user_from_org_manager(instance)
