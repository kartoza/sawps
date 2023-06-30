from rest_framework import serializers

from species.models import Taxon


class TaxonSerializer(serializers.ModelSerializer):
    """Species serializer"""

    class Meta():
        model = Taxon
        fields = "__all__"