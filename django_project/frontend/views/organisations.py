import json
from sawps.views import AddUserToOrganisation
from .base_view import RegisteredOrganisationBaseView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class OrganisationsView(
    LoginRequiredMixin,
    RegisteredOrganisationBaseView,
    TemplateView
):
    """
    OrganisationsView displays the organisations the
    user can access.
    """
    template_name = 'organisations.html'
    context_object_name = 'organisations'


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
