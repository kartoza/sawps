from django.urls import path
from sawps.views import ActivateAccount,SendRequestEmail

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
    path(
        'sendrequest/',
        SendRequestEmail.as_view(),
        name='sendrequest',
    )
]
