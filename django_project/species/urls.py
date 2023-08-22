from django.urls import path
from species.api_views.upload_species import SaveCsvSpecies, SpeciesUploader

from .views import TaxonFrontPageListAPIView, TaxonListAPIView

urlpatterns = [
    path('api/species/front-page/list/', TaxonFrontPageListAPIView.as_view(),
         name='species-front-page'),
    path('species/', TaxonListAPIView.as_view(),
         name='species'),
    path('api/upload-species/', SpeciesUploader.as_view(),
         name='upload-species'),
    path('api/save-csv-species/', SaveCsvSpecies.as_view(),
         name='save-csv-species'),

]
