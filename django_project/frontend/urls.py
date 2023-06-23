"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views.home import HomeView
from .views.map import MapView
from .views.help import HelpView
from .views.about import AboutView
from .views.contact import ContactView

from frontend.api_views.map import (
    ContextLayerList,
    MapStyles,
    AerialTile,
    PropertiesLayerMVTTiles,
    FindParcelByCoord,
    FindPropertyByCoord,
    MapAuthenticate
)
from frontend.api_views.property import (
    CreateNewProperty,
    PropertyMetadataList,
    PropertyList,
    UpdatePropertyInformation,
    UpdatePropertyBoundaries,
    PropertyDetail
)
from frontend.api_views.upload import (
    BoundaryFileUpload,
    BoundaryFileRemove,
    BoundaryFileList,
    BoundaryFileSearch,
    BoundaryFileSearchStatus
)

urlpatterns = [
    re_path(
        r'^api/map/search/parcel/?$',
        FindParcelByCoord.as_view(),
        name='find-parcel'
    ),
    re_path(
        r'^api/map/search/property/?$',
        FindPropertyByCoord.as_view(),
        name='find-property'
    ),
    re_path(
        r'^api/map/search/context_layer/list/?$',
        ContextLayerList.as_view(),
        name='context-layer-list'
    ),
    re_path(
        r'^api/map/styles/?$',
        MapStyles.as_view(),
        name='map-style'
    ),
    re_path(
        r'^api/map/authenticate/?$',
        MapAuthenticate.as_view(),
        name='map-authenticate'
    ),
    re_path(
        r'^api/map/layer/aerial/'
        r'(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/?$',
        AerialTile.as_view(),
        name='aerial-map-layer'
    ),
    re_path(
        r'^api/map/layer/properties/'
        r'(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/?$',
        PropertiesLayerMVTTiles.as_view(),
        name='properties-map-layer'
    ),
    re_path(
        r'^api/property/create/?$',
        CreateNewProperty.as_view(),
        name='property-create'
    ),
    re_path(
        r'^api/property/list/?$',
        PropertyList.as_view(),
        name='property-list'
    ),
    re_path(
        r'^api/property/detail/(?P<id>\d+)/?$',
        PropertyDetail.as_view(),
        name='property-detail'
    ),
    re_path(
        r'^api/property/detail/update/?$',
        UpdatePropertyInformation.as_view(),
        name='property-update-detail'
    ),
    re_path(
        r'^api/property/boundaries/update/?$',
        UpdatePropertyBoundaries.as_view(),
        name='property-update-boundaries'
    ),
    re_path(
        r'^api/property/metadata/list/?$',
        PropertyMetadataList.as_view(),
        name='property-metadata'
    ),
    re_path(
        r'^api/upload/boundary-file/remove/?$',
        BoundaryFileRemove.as_view(),
        name='boundary-file-remove'
    ),
    re_path(
        r'^api/upload/boundary-file/(?P<session>[\da-f-]+)/list/?$',
        BoundaryFileList.as_view(),
        name='boundary-file-list'
    ),
    re_path(
        r'^api/upload/boundary-file/(?P<session>[\da-f-]+)/search/?$',
        BoundaryFileSearch.as_view(),
        name='boundary-file-search'
    ),
    re_path(
        r'^api/upload/boundary-file/(?P<session>[\da-f-]+)/status/?$',
        BoundaryFileSearchStatus.as_view(),
        name='boundary-file-status'
    ),
    re_path(
        r'^api/upload/boundary-file/?$',
        BoundaryFileUpload.as_view(),
        name='boundary-file-upload'
    ),
    path('map/', MapView.as_view(), name='map'),
    path('help/', HelpView.as_view(), name='help'),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]
