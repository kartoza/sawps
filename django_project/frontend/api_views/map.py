"""API Views related to map."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from frontend.models.context_layer import ContextLayer
from frontend.serializers.context_layer import ContextLayerSerializer


class ContextLayerList(APIView):
    """Fetch context layers."""
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Retrieve all context layers."""
        layers = ContextLayer.objects.all().order_by('id')
        return Response(
            status=200,
            data=ContextLayerSerializer(layers, many=True).data
        )


class MapStyles(APIView):
    """Fetch map styles."""


class PropertiesLayerMVTTiles(APIView):
    """Dynamic Vector Tile for properties layer."""
