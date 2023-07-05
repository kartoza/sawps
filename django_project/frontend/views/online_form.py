from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from .base_view import RegisteredOrganisationBaseView
from property.models import Property


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
        ctx['property_id'] = property_id
        return ctx
