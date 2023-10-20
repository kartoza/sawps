from django.urls import path, re_path
from species.api_views.upload_species import (
    SaveCsvSpecies,
    SpeciesUploader,
    UploadSpeciesStatus,
)

from .views import (
    TaxonFrontPageListAPIView,
    TaxonListAPIView,
    TaxonTrendPageListAPIView
)

urlpatterns = [
    path('api/species/front-page/list/', TaxonFrontPageListAPIView.as_view(),
         name='species-front-page'),
    path(r'^api/species/trend-page/(?P<species_id>\d+)/?$', TaxonTrendPageListAPIView.as_view(),
         name='species-trend-page'),
    path('species/', TaxonListAPIView.as_view(),
         name='species'),
    path('api/upload-species/', SpeciesUploader.as_view(),
         name='upload-species'),
    path('api/save-csv-species/', SaveCsvSpecies.as_view(),
         name='save-csv-species'),
    re_path(r'api/upload-species-status/(?P<token>[\da-f-]+)/?$',
            UploadSpeciesStatus.as_view(),
            name='upload-species-status'
            ),

]
