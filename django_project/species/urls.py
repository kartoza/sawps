from django.urls import path, include


# api urls
urlpatterns = [  # '',
    path('api/', include('species.api_urls')),
]