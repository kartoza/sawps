from . import models
from . import serializers
import rest_framework.generics as generics
from rest_framework.permissions import IsAdminUser, AllowAny


class WMSLayerCreateView(generics.ListCreateAPIView):
    """creating wms layers"""

    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """overriding get_queryset method"""
        return models.WMS.objects.all()


class WMSLayerUpdateView(generics.RetrieveUpdateAPIView):
    """updating wms layers"""

    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return models.WMS.objects.all()


class WMSLayerDeleteView(generics.RetrieveDestroyAPIView):
    """deleting wms layers"""

    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return models.WMS.objects.all()


class WMSLayersListView(generics.ListAPIView):
    """List WMS layers"""

    serializer_class = serializers.WMSLayerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """overriding get_queryset method"""
        return models.WMS.objects.all()


class WMSLayerDetailedView(generics.RetrieveAPIView):
    """view for rud opertaions over a single WMS layer"""

    serializer_class = serializers.WMSLayerSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [AllowAny]

    def get_queryset(self):
        return models.WMS.objects.all()
