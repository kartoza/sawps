from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from .base_view import RegisteredOrganisationBaseView
from property.models import Property
from stakeholder.models import OrganisationUser


class OnlineFormView(LoginRequiredMixin, RegisteredOrganisationBaseView):
    """
    OnlineFormView displays the page to upload species data.
    """

    template_name = 'online_form.html'

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
        return ctx
