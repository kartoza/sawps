from rest_framework import serializers
from species.models import Taxon


class TaxonSerializer(serializers.ModelSerializer):
    """Species serializer"""

    class Meta():
        model = Taxon
        fields = ['id', 'common_name_varbatim', "scientific_name"]
