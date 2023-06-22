"""View to switch organisation."""
from django.http import HttpResponseRedirect
from stakeholder.models import OrganisationUser
from frontend.views.base_view import (
    CURRENT_ORGANISATION_ID_KEY,
    CURRENT_ORGANISATION_KEY
)

def switch_organisation(request, organisation_id):
    """Switch organisation."""
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if organisation_id:
        # validate if user belongs to organisation
        organisation_user = OrganisationUser.objects.filter(
            user=request.user,
            organisation__id=organisation_id
        )
        if not organisation_user.exists():
            return HttpResponseRedirect('/')
        # store new organisation in the session
        organisation = organisation_user.first().organisation
        request.session[
            CURRENT_ORGANISATION_ID_KEY] = organisation.id
        request.session[
            CURRENT_ORGANISATION_KEY] = organisation.name
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)
