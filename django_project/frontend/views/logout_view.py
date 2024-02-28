from allauth.account.views import LogoutView
from .base_view import OrganisationBaseView


class LogoutView(OrganisationBaseView, LogoutView):
    """
    LogoutView displays the logout page by rendering
    the 'account/logout.html' template.
    """

    template_name = 'account/logout.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
