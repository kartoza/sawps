from stakeholder.models import UserProfile

"""Organisation utility functions."""

CURRENT_ORGANISATION_ID_KEY = 'current_organisation_id'
CURRENT_ORGANISATION_KEY = 'current_organisation'


def get_current_organisation_id(user):
    try:
        user_profile = user.user_profile
        if user_profile.current_organisation:
            return user_profile.current_organisation.id
    except UserProfile.DoesNotExist:
        return None
