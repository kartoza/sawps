from django.urls import path, include
from swaps.views import ProfileView


# views urls
urlpatterns = [  # '',
    path('profile/', ProfileView.as_view(),
        name='profile'),

]
