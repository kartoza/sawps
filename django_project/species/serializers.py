from rest_framework import serializers
from swaps.models import UploadSession


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
