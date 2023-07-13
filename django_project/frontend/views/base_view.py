"""Provide classes for base view."""
from django.views.generic import TemplateView
from stakeholder.models import OrganisationUser, Organisation
from frontend.serializers.stakeholder import OrganisationSerializer
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
    CURRENT_ORGANISATION_KEY
)


class RegisteredOrganisationBaseView(TemplateView):
    """
    Base view to provide organisation context for logged-in users.
    """

    def set_current_organisation(self, organisation: Organisation):
        if organisation:
            self.request.session[
                CURRENT_ORGANISATION_ID_KEY] = organisation.id
            self.request.session[
                CURRENT_ORGANISATION_KEY] = organisation.name
        else:
            self.request.session[
                CURRENT_ORGANISATION_ID_KEY] = 0
            self.request.session[
                CURRENT_ORGANISATION_KEY] = ''


    def get_or_set_current_organisation(self):
        if (
            CURRENT_ORGANISATION_ID_KEY in self.request.session and
            CURRENT_ORGANISATION_KEY in self.request.session
        ):
            return (
                self.request.session[CURRENT_ORGANISATION_ID_KEY],
                self.request.session[CURRENT_ORGANISATION_KEY]
            )
        organisation: Organisation = None
        if self.request.user.is_superuser:
            organisation = Organisation.objects.all().order_by('name').first()
        else:
            organisation_user = OrganisationUser.objects.filter(
                user=self.request.user
            ).select_related('organisation').order_by(
                'organisation__name'
            ).first()
            if organisation_user:
                organisation = organisation_user.organisation
        self.set_current_organisation(organisation)
        return (
            organisation.id, organisation.name
        ) if organisation else (0, '')

    def get_organisation_list(self):
        if self.request.user.is_superuser:
            # fetch all organisations
            organisations = Organisation.objects.all().order_by('name')
            if CURRENT_ORGANISATION_ID_KEY in self.request.session:
                organisations = organisations.exclude(
                    id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
            return OrganisationSerializer(organisations, many=True).data
        # non-superuser organisations
        user_organisations = OrganisationUser.objects.filter(
            user=self.request.user
        ).order_by('organisation_id').values_list(
            'organisation_id', flat=True
        ).distinct()
        organisations = Organisation.objects.filter(
            id__in=user_organisations
        ).order_by('name')
        if CURRENT_ORGANISATION_ID_KEY in self.request.session:
            organisations = organisations.exclude(
                id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
        return OrganisationSerializer(organisations, many=True).data



    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return ctx
        current_organisation_id, current_organisation = (
            self.get_or_set_current_organisation()
        )
        # fetch organisation list
        ctx['current_organisation'] = (
            current_organisation if current_organisation else '-'
        )
        ctx['current_organisation_id'] = current_organisation_id
        ctx['organisations'] = self.get_organisation_list()
        return ctx
