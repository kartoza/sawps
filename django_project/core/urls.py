"""Core URL Configuration.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from docs_crawler.urls import preferences as docs_crawler_preferences
from sawps.custom_docs_crawler_views import CustomDocumentationDetail

urlpatterns = [
    path('accounts/two-factor/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('frontend.urls')),
    path('admin/', admin.site.urls),
    path('', include('notification.urls')),
    path('', include('activity.urls')),
    path('', include('stakeholder.urls')),
    path('', include('sawps.urls')),
    path('', include('species.urls')),
]

# Docs crawler
urlpatterns += [
    path(
        'admin/docs_crawler/preferences/',
        docs_crawler_preferences,
        name='docs-crawler-admin-preferences'
    ),
    path('docs_crawler/data/',
         CustomDocumentationDetail.as_view(),
         name='docs-crawler-data'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
