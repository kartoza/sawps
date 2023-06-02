from django.urls import re_path, include
from swaps.views import ProfileView


# views urls
urlpatterns = [  # '',
    re_path(r'^profile/(?P<slug>\w+)/$', ProfileView.as_view(),
        name='profile'),

]
