from stakeholder.models import UserProfile, OrganisationUser

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


def get_abbreviation(text: str):
    """
    Get abbreviation from text.
    """
    words = text.split(' ')
    if len(words) == 1:
        return words[0][0:2].upper()
    else:
        return ''.join(map(lambda word: word[0:1].upper(), words))


def get_organisation_ids(user):
    """Get organisation ids that user belongs to."""
    return OrganisationUser.objects.filter(
        user=user
    ).values_list('organisation_id', flat=True)
