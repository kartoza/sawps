from django.urls import path
from swaps.views import ActivateAccount

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateAccount.as_view(),
        name='activate',
    ),
]
