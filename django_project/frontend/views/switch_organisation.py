"""View to switch organisation."""
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden
)
from django.shortcuts import get_object_or_404

from stakeholder.models import (
    OrganisationUser,
    Organisation
)


@login_required
def switch_organisation(request, organisation_id):
    """Switch organisation."""
    organisation = get_object_or_404(
        Organisation,
        id=organisation_id
    )

    # Validate if the user can switch organisations
    # only if the user is not a superadmin
    if not request.user.is_superuser:
        organisation_user = OrganisationUser.objects.filter(
            user=request.user,
            organisation__id=organisation_id
        )
        if not organisation_user.exists():
            return HttpResponseForbidden()

    # Update the current organisation in the user's profile
    user_profile = request.user.user_profile
    user_profile.current_organisation = organisation
    user_profile.save()

    # Redirect to the specified 'next' URL
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)
