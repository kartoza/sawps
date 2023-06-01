from django.urls import path, include


# api urls
urlpatterns = [  # '',
    path('api/', include('swaps.api_urls')),

]
