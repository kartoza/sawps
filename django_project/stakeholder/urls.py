from django.contrib.auth.decorators import login_required
from django.urls import re_path, reverse_lazy, path
from django.views.generic import RedirectView
from stakeholder.views import (
    ProfileView,
    RemindersView,
    NotificationsView,
    check_email_exists,
    OrganisationAPIView,
)

# views urls
urlpatterns = [  # '',
    path(
        'profile/<str:slug>/',
        ProfileView.as_view(),
        name='profile'
    ),
    re_path(
        r'^profile/$',
        login_required(
            lambda request: RedirectView.as_view(
                url=reverse_lazy(
                    'profile',
                    kwargs={'slug': request.user.username}
                ),
                permanent=False,
            )(request)
        ),
        name='profile-settings',
    ),
    path(
        'reminders/<str:slug>/',
        RemindersView.as_view(),
        name='reminders'
    ),
    path(
        'notifications/<str:slug>/',
        NotificationsView.as_view(),
        name='notifications'
    ),
    path(
        'check_email_exists/',
        check_email_exists,
        name='check_email_exists'
    ),
    path(
        'api/organisation/',
        OrganisationAPIView.as_view(),
        name='organisation'
    )
]
