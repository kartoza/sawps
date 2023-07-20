from django.urls import path
from sawps.views import (
    ActivateAccount,
    SendRequestEmail,
    AddUserToOrganisation
)

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
    path(
        'adduser/<user_email>/<organisation>/',
        AddUserToOrganisation.as_view(),
        name='adduser'
    ),
    path(
        'sendrequest/',
        SendRequestEmail.as_view(),
        name='sendrequest',
    )
]
