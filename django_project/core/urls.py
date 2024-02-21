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

urlpatterns = [
    path('accounts/two-factor/', include('frontend.allauth2fa_urls')),
    path('accounts/two-factor/', include('allauth_2fa.urls')),
    path('accounts/logout/', include('frontend.accounts_urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('frontend.urls')),
    path('', include('docs_crawler.urls')),
    path('admin/', admin.site.urls),
    path('', include('notification.urls')),
    path('', include('activity.urls')),
    path('', include('stakeholder.urls')),
    path('', include('sawps.urls')),
    path('', include('species.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
