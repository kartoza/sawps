from django.urls import path
from species.api_views.upload_species import SpeciesUploader


urlpatterns = [
    path('upload-species/', SpeciesUploader.as_view(), name='upload-species'),
]