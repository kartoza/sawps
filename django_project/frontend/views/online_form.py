from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from .base_view import RegisteredOrganisationBaseView
from property.models import Property
from stakeholder.models import OrganisationUser, OrganisationRepresentative
from population_data.models import AnnualPopulation


class OnlineFormView(RegisteredOrganisationBaseView):
    """
    OnlineFormView displays the page to upload species data.
    """

    template_name = 'online_form.html'

    def validate_data_edit_access(self, upload: AnnualPopulation, user):
        # validate if user is data owner or manager
        if user.is_superuser:
            return True
        is_manager = OrganisationRepresentative.objects.filter(
            user=user,
            organisation=upload.property.organisation
        ).exists()
        if is_manager:
            return True
        return upload.user.id == user.id

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['maptiler_api_key'] = settings.MAPTILER_API_KEY
        property_id = kwargs.get('property_id')
        property = get_object_or_404(Property, id=property_id)
        # validate user belongs to property organisation
        if not self.request.user.is_superuser:
            valid = OrganisationUser.objects.filter(
                organisation=property.organisation,
                user=self.request.user
            ).exists()
            if not valid:
                raise PermissionDenied()
        ctx['property_id'] = property_id
        # check if upload is belong to property
        ctx['upload_id'] = 0
        upload_id = self.request.GET.get('upload_id', 0)
        if upload_id:
            valid_upload = AnnualPopulation.objects.filter(
                id=upload_id,
                property_id=property_id
            ).first()
            if valid_upload:
                if (
                    not self.validate_data_edit_access(
                        valid_upload, self.request.user)
                ):
                    raise PermissionDenied()
                ctx['upload_id'] = valid_upload.id
        return ctx
