from django.urls import path
from .views import TaxonListAPIView

urlpatterns = [
    path('species/',TaxonListAPIView.as_view(),name='species'),
    ]
