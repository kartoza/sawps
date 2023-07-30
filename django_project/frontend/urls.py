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
from frontend.views.base_view import get_user_notifications
from frontend.api_views.data_table import DataTableAPIView
from frontend.api_views.map import (
    AerialTile,
    ContextLayerList,
    FindParcelByCoord,
    FindPropertyByCoord,
    MapAuthenticate,
    MapStyles,
    PropertiesLayerMVTTiles,
)
from frontend.api_views.metrics import (
    ActivityPercentageAPIView,
    SpeciesPopulationCountAPIView,
)
from frontend.api_views.population import (
    DraftPopulationUpload,
    FetchDraftPopulationUpload,
    PopulationMetadataList,
    UploadPopulationAPIVIew,
)
from frontend.api_views.property import (
    CreateNewProperty,
    PropertyDetail,
    PropertyList,
    PropertyMetadataList,
    UpdatePropertyBoundaries,
    UpdatePropertyInformation,
)
from frontend.api_views.upload import (
    BoundaryFileList,
    BoundaryFileRemove,
    BoundaryFileSearch,
    BoundaryFileSearchStatus,
    BoundaryFileUpload,
)

from .views.about import AboutView
from .views.contact import ContactUsView
from .views.help import HelpView
from .views.home import HomeView
from .views.map import MapView
from .views.online_form import OnlineFormView
from .views.switch_organisation import switch_organisation
from .views.users import OrganisationUsersView

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
    re_path(
        r'^api/population/metadata/list/?$',
        PopulationMetadataList.as_view(),
        name='population-metadata'
    ),
    re_path(
        r'^api/upload/population/(?P<property_id>\d+)/?$',
        UploadPopulationAPIVIew.as_view(),
        name='population-upload'
    ),
    path(
        'api/upload/population/draft/<uuid:draft_uuid>/',
        FetchDraftPopulationUpload.as_view(),
        name='fetch-draft-upload-species'
    ),
    path(
        'api/upload/population/draft/<int:property_id>/',
        DraftPopulationUpload.as_view(),
        name='draft-upload-species'
    ),
    path(
        'switch-organisation/<int:organisation_id>/',
        switch_organisation,
        name='switch-organisation'
    ),
    path('map/', MapView.as_view(), name='map'),
    path(
        'upload-data/<int:property_id>/',
        OnlineFormView.as_view(),
        name='online-form'
    ),
    path('help/', HelpView.as_view(), name='help'),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('users/', OrganisationUsersView.as_view(), name='Users'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('data-table/', DataTableAPIView.as_view(), name='data-table'),
    path(
        'species-population-count/<int:property_id>/',
        SpeciesPopulationCountAPIView.as_view(),
        name='species_population_count'
    ),
    path(
        'activity-percentage/',
        ActivityPercentageAPIView.as_view(),
        name='activity_percentage'
    ),
    path(
        'get_user_notifications/',
        get_user_notifications,
        name='get_user_notifications'
    )
]
