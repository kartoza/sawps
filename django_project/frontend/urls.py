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
from frontend.api_views.map import (
    ContextLayerList,
    MapStyles,
    AerialTile,
    FindParcelByCoord
)

urlpatterns = [
    re_path(
         r'^api/map/search/parcel/?$',
        FindParcelByCoord.as_view(),
        name='find-parcel'),
    re_path(
         r'^api/map/search/context_layer/list/?$',
        ContextLayerList.as_view(),
        name='context-layer-list'),
    re_path(
         r'^api/map/styles/?$',
        MapStyles.as_view(),
        name='map-style'),
    re_path(
         r'^api/map/aerial/'
         r'(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/?$',
        AerialTile.as_view(),
        name='aerial-map-tile'),
    path('map/', MapView.as_view(), name='map'),
    path('', HomeView.as_view(), name='home'),
]
