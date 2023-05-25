from django.urls import path
from . import views

urlpatterns = [
    path('vector_layers', views.VectorLayersListView.as_view(), name = 'list_vector_layers'),
    path('vector_layer/<int:id>', views.VectorLayerDetailedView.as_view(), name = 'get_vector_layer'),
    path('features', views.FeaturesListView.as_view(), name = 'list_features'),
    path('feature/<int:id>', views.FeatureDetailedView.as_view(), name = 'get_feature'),
    path('wms', views.WMSLayersListView.as_view(), name = 'list_wms_layers'),
    path('wms/<int:id>', views.WMSLayerDetailedView.as_view(), name = 'get_wms_layer'),
    path('raster_layer', views.RasterLayersListView.as_view(), name = 'list_raster_layers'),
    path('raster_layer/<int:id>', views.RasterLayerDetailedView.as_view(), name = 'get_raster_layer'),
]
