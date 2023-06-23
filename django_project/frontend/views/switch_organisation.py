"""View to switch organisation."""
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from stakeholder.models import OrganisationUser, Organisation
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
    CURRENT_ORGANISATION_KEY
)


@login_required
def switch_organisation(request, organisation_id):
    """Switch organisation."""
    organisation = get_object_or_404(
        Organisation,
        id=organisation_id
    )
    # validate if user can switch org only if user is not superadmin
    if not request.user.is_superuser:
        organisation_user = OrganisationUser.objects.filter(
            user=request.user,
            organisation__id=organisation_id
        )
        if not organisation_user.exists():
            return HttpResponseForbidden()
    # store new organisation in the session
    request.session[
        CURRENT_ORGANISATION_ID_KEY] = organisation.id
    request.session[
        CURRENT_ORGANISATION_KEY] = organisation.name
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)
