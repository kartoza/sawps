from django.urls import path, include
from .views import TaxonListAPIView, SpeciesForm

urlpatterns = [
    path('species/', TaxonListAPIView.as_view(), name='species'),
    path('api/', include('species.api_urls')),
     path('species-form/', SpeciesForm.as_view(), name='species-from'),
]