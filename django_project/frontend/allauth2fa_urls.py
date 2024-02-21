from django.urls import path
from frontend.views.allauth_2fa import (
    BackupTokensView,
    SetupTwoFactorView,
    RemoveTwoFactorView
)

urlpatterns = [
    path(
        "setup/",
        SetupTwoFactorView.as_view(),
        name="two-factor-setup",
    ),
    path(
        "backup-tokens/",
        BackupTokensView.as_view(),
        name="two-factor-backup-tokens",
    ),
    path(
        "remove/",
        RemoveTwoFactorView.as_view(),
        name="two-factor-remove",
    ),
]
