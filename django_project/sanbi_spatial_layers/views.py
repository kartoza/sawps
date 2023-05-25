from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny


class VectorLayersListView(ListCreateAPIView):
    """ view for bulk operations over vector layers  """
    serializer_class = serializers.VectorLayerSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        """ overriding get_queryset method """
        return models.VectorLayer.objects.all()

class VectorLayerDetailedView(RetrieveUpdateDestroyAPIView):
    """ view for rud opertaions over a single vector layer """
    serializer_class = serializers.VectorLayerSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = "id"
    # queryset = models.VectorLayer.objects.all()
    def get_queryset(self):
      return models.VectorLayer.objects.all() 

class FeaturesListView(ListCreateAPIView):
    """ view for bulk operations over features  """
    serializer_class = serializers.FeatureSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return models.Feature.objects.all()

class FeatureDetailedView(RetrieveUpdateDestroyAPIView):
    """ view for rud opertaions over a single feature """
    serializer_class = serializers.FeatureSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = "id"

    def get_queryset(self):
      return models.Feature.objects.all() 

class WMSLayersListView(ListCreateAPIView):
    """ view for bulk operations over WMS layers  """
    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        """ overriding get_queryset method """
        return models.WMS.objects.all()

class WMSLayerDetailedView(RetrieveUpdateDestroyAPIView):
    """ view for rud opertaions over a single WMS layer """
    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = "id"
    def get_queryset(self):
      return models.WMS.objects.all() 


class RasterLayersListView(ListCreateAPIView):
    """ view for bulk operations over Raster layers  """
    serializer_class = serializers.RasterLayerSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        """ overriding get_queryset method """
        return models.RasterLayer.objects.all()

class RasterLayerDetailedView(RetrieveUpdateDestroyAPIView):
    """ view for rud opertaions over a single Raster layer """
    serializer_class = serializers.RasterLayerSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = "id"
    # queryset = models.RasterLayer.objects.all()
    def get_queryset(self):
      return models.RasterLayer.objects.all() 


