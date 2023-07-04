from django.urls import path
from .views import TaxonView

urlpatterns = [
    path('species/',TaxonView.as_view(),name='species'),
    ]
