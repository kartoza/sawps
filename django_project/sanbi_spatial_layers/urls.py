from django.urls import path
from . import views

urlpatterns = [
    path('wms', views.WMSLayersListView.as_view(), name='list_wms_layers'),
    path('wms/add', views.WMSLayerCreateView.as_view(), name='add_wms_layer'),
    path(
        'wms/edit/<int:id>',
        views.WMSLayerUpdateView.as_view(),
        name='edit_wms_layer',
    ),
    path(
        'wms/delete/<int:id>',
        views.WMSLayerDeleteView.as_view(),
        name='delete_wms_layer',
    ),
    path(
        'wms/<int:id>',
        views.WMSLayerDetailedView.as_view(),
        name='get_wms_layer',
    ),
]
