from typing import List

from django.contrib.auth.models import User

from frontend.static_mapping import SUPER_USER


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

    return roles
