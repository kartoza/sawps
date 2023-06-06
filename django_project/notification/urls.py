from django.urls import path, include


# api urls
urlpatterns = [  # '',
    path('api/', include('notification.api_urls')),

]
