from django.urls import path
from .views import TaxonListAPIView, TaxonFrontPageListAPIView

urlpatterns = [
    path('api/species/front-page/list/', TaxonFrontPageListAPIView.as_view(),
         name='species-front-page'),
    path('species/', TaxonListAPIView.as_view(), name='species'),
]
