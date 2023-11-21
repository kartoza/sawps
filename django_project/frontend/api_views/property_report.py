from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from property.models import Property

PROPERTY_INFORMATION = 'Property Information'


class PropertyInformationSerializer(serializers.ModelSerializer):

    property_name = serializers.CharField(source='name')
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj: Property):
        if obj.owner_email:
            try:
                return User.objects.get(
                    email=obj.owner_email
                ).first_name
            except User.DoesNotExist:
                return obj.owner_email
        return '-'

    class Meta:
        model = Property
        fields = [
            'property_name',
            'owner'
        ]


class PropertyReportApiView(APIView):
    """
    API view for retrieving data table for property report.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        properties = Property.objects.all()
        return Response(
            {
                PROPERTY_INFORMATION: PropertyInformationSerializer(
                    properties,
                    many=True
                ).data
            }
        )
