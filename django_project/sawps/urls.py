from django.urls import path
from sawps.views import (
    ActivateAccount,
    SendRequestEmail,
    AddUserToOrganisation,
    CustomPasswordResetView,
    custom_password_reset_complete_view,
    health, resend_verification_email
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
    path(
        'adduser/<invitation_uuid>/',
        AddUserToOrganisation.as_view(),
        name='adduser'
    ),
    path(
        'sendrequest/',
        SendRequestEmail.as_view(),
        name='sendrequest',
    ),
    path(
        'password_reset/',
        CustomPasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='forgot_password_reset.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        custom_password_reset_complete_view,
        name='password_reset_complete'
    ),
    path(
        'healthz/',
        health,
        name='healthz'
    ),
    path('accounts/resend-verification/',
         resend_verification_email,
         name='account_resend_verification'),
]
