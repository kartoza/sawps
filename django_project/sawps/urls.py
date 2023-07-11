from django.urls import path
from sawps.views import ActivateAccount,AddUserToOrganisation

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
    path(
        'adduser/<uidb64>/<organisation>/',
        AddUserToOrganisation.as_view(),
        name='adduser',
    ),
]
