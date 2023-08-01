from rest_framework import serializers
from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPDeviceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = TOTPDevice
        fields = [
            'id',
            'user',
            'name',
        ]
