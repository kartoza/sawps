from django.urls import path
from sawps.views import ActivateAccount

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
]
