from typing import List

from django.contrib.auth.models import User

from frontend.static_mapping import (
    SUPER_USER,
    ORGANISATION_MEMBER,
    ORGANISATION_MANAGER
)
from stakeholder.models import (
    OrganisationUser, OrganisationInvites, MANAGER, UserProfile
)


def is_organisation_member(user: User) -> bool:
    """
    Determine if a user is a member of the currently active organisation.

    :param user: The user object
    :return:  True if the user is a member, otherwise False
    """
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


def is_organisation_manager(user: User) -> bool:
    """
    Determine if a user is a manager of the currently active organisation.

    :param user: The user object
    :return: True if the user is a manager, otherwise False
    """
    if not UserProfile.objects.filter(
            user=user
    ).exists():
        return False

    if not user.user_profile.current_organisation:
        return False

    # TODO: Add the user object to organisation invites,
    #  because users can change their email.
    return OrganisationInvites.objects.filter(
        email=user.email,
        organisation=user.user_profile.current_organisation,
        assigned_as=MANAGER
    ).exists()


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
