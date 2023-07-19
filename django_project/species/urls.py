from django.urls import path, include
from .views import TaxonListAPIView

urlpatterns = [
    path('species/', TaxonListAPIView.as_view(), name='species'),
    path('api/', include('species.api_urls')),
]