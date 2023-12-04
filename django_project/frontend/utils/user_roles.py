from typing import List, Set

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from frontend.static_mapping import (
    SUPER_USER,
    ORGANISATION_MEMBER,
    ORGANISATION_MANAGER,
    DATA_CONSUMERS,
    DATA_CONSUMERS_EXCLUDE_PERMISSIONS
)
from stakeholder.models import (
    OrganisationUser, OrganisationInvites, MANAGER, UserProfile, Organisation
)
from frontend.utils.organisation import get_current_organisation_id
from sawps.models import ExtendedGroup


def is_organisation_member(user: User) -> bool:
    """
    Determine if a user is a member of the currently active organisation.

    :param user: The user object
    :return:  True if the user is a member, otherwise False
    """

    # TODO: Update organisation member checking to use group
    # Since user with OrganisationUser record will be added to
    # organisation member/manager group.
    if not UserProfile.objects.filter(
        user=user
    ).exists():
        return False
    if not user.user_profile.current_organisation:
        return False

    return OrganisationUser.objects.filter(
        user=user,
        organisation=user.user_profile.current_organisation
    ).exists()


def is_organisation_manager(
        user: User, organisation: Organisation = None) -> bool:
    """
    Determines whether a user is a manager of the currently active organisation
    or of the organisation specified as a parameter, if provided.

    :param user: The user object to check.
    :param organisation: Optional organisation object to check against.
    :return: True if the user is a manager of the organisation,
        otherwise False.
    """

    # Since user with OrganisationUser record will be added to
    # organisation member/manager group, use group to check role.

    if not UserProfile.objects.filter(
            user=user
    ).exists():
        return False

    if not user.user_profile.current_organisation and not organisation:
        return False

    # TODO: Add the user object to organisation invites,
    #  because users can change their email.
    org_invite_exists = OrganisationInvites.objects.filter(
        email=user.email,
        organisation=(
            organisation if organisation else
            user.user_profile.current_organisation
        ),
        assigned_as=MANAGER
    ).exists()
    group_exists = 'Organisation Manager'.lower() in [
        name.lower() for name in user.groups.values_list('name', flat=True)
    ]
    return org_invite_exists or group_exists


def get_user_roles(user: User) -> List[str]:
    """
    Retrieve the roles associated with a given user.

    :param user: The user object
    :return: A list containing the names of all
        roles associated with the user
    """
    roles = list(
        user.groups.all().values_list(
            'name', flat=True
        )
    )
    if user.is_superuser:
        roles += [SUPER_USER]

    if is_organisation_member(user):
        roles += [ORGANISATION_MEMBER]

    if is_organisation_manager(user):
        roles += [ORGANISATION_MANAGER]

    return roles


def get_user_permissions(user: User) -> Set[str]:
    """
    Retrieve the permissions associated with a given user.

    :param user: The user object
    :return: A set containing the names of all
        permissions associated with the user
    """
    permissions = set()
    groups = user.groups.all()
    content_type = ContentType.objects.get_for_model(ExtendedGroup)
    ext_group_permissions = Permission.objects.filter(
        content_type=content_type
    )
    organisation_id = get_current_organisation_id(user)
    if organisation_id:
        organisation = Organisation.objects.get(id=organisation_id)
        if organisation.national:
            permissions.add('Can view province report')

    if user.is_superuser:
        ext_group_permissions_set = set(
            ext_group_permissions.values_list('name', flat=True)
        )
        permissions = permissions.union(ext_group_permissions_set)
        permissions.add('Can view province report')

    for group in groups:
        allowed_permission = set(
            group.permissions.filter(
                id__in=ext_group_permissions
            ).values_list('name', flat=True)
        )
        permissions = permissions.union(allowed_permission)

    if not user.is_superuser:
        user_roles = get_user_roles(user)
        if set(user_roles) & set(DATA_CONSUMERS):
            permissions = (
                permissions - DATA_CONSUMERS_EXCLUDE_PERMISSIONS
            )

    return permissions


def check_user_has_permission(user: User, permission: str):
    """
    Test if a user has permission.
    """
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permission in permissions
