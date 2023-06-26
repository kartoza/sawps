from django.contrib.auth.decorators import login_required
from django.urls import re_path, reverse_lazy, path
from django.views.generic import RedirectView
from stakeholder.views import ProfileView


# views urls
urlpatterns = [  # '',
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    re_path(
        r'^profile/$',
        login_required(
            lambda request: RedirectView.as_view(
                url=reverse_lazy(
                    'profile', kwargs={'slug': request.user.username}
                ),
                permanent=False,
            )(request)
        ),
        name='profile-settings',
    ),
    ]