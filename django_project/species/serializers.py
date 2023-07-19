from rest_framework import serializers
from species.models import Taxon
from swaps.models import UploadSession


class TaxonSerializer(serializers.ModelSerializer):
    """Species serializer"""

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(TaxonSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta():
        model = Taxon
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
