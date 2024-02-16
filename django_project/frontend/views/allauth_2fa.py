from allauth_2fa.views import (
    TwoFactorBackupTokens,
    TwoFactorSetup,
    TwoFactorRemove
)
from .base_view import OrganisationBaseView


class BackupTokensView(TwoFactorBackupTokens, OrganisationBaseView):
    """
    BackupTokensView appends organisations context data from allauth-2fa.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SetupTwoFactorView(TwoFactorSetup, OrganisationBaseView):
    """
    SetupTwoFactorView appends organisations context data from allauth-2fa.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RemoveTwoFactorView(TwoFactorRemove, OrganisationBaseView):
    """
    RemoveTwoFactorView appends organisations context data from allauth-2fa.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
