from django.urls import path
from frontend.views.logout_view import LogoutView


urlpatterns = [
    path('', LogoutView.as_view(), name='logout')
]
