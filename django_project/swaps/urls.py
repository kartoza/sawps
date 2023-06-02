from django.urls import path, include
from swaps.views import ProfileView


# views urls
urlpatterns = [  # '',
    path('<slug:slug>', ProfileView.as_view(),
        name='profile'),

]
