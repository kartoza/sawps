# In your Django view or viewset
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.sites.models import Site
from frontend.serializers.totp_device import TOTPDeviceSerializer
from base64 import b32encode
from io import BytesIO
from urllib.parse import quote
from urllib.parse import urlencode
import qrcode
import base64


def return_json(object):
    return JsonResponse(
        {
            'status': 'success',
            'totp_devices': object
        }
    )


def generate_qr_code(otpauth_url):
    img = qrcode.make(
        otpauth_url,
        image_factory=qrcode.image.svg.SvgPathImage
    )
    io = BytesIO()
    img.save(io)
    qr_code_base64 = base64.b64encode(io.getvalue()).decode()
    return qr_code_base64


def generate_qrcode(device):
    params = {
        "secret": b32encode(device.bin_key).decode("utf-8"),
        "algorithm": "SHA1",
        "digits": device.digits,
        "period": device.step,
        "issuer": Site.objects.get_current().domain,
    }

    label = str(device.user.username)

    otpauth_url = f"otpauth://totp/{quote(label)}?{urlencode(params)}"

    qr_code_base64 = generate_qr_code(otpauth_url)

    return [
        {
            'id': device.id,
            'name': device.name,
            'user': device.user.username,
            'qrcode': qr_code_base64
        }]


def view_totp_devices(request):
    user = request.user

    # Fetch all TOTP devices for the user
    totp_devices = TOTPDevice.objects.filter(user=user.id)

    serialized_devices = TOTPDeviceSerializer(
                    totp_devices, many=True)

    return return_json(serialized_devices.data)


def add_totp_device(request):
    if request.method == 'POST':
        user = request.user

        device_name = request.POST.get('device_name', '')

        device = TOTPDevice(
            user=user,
            name=device_name
        )
        device.save()

        return_device = generate_qrcode(device)

        return return_json(return_device)
    return return_json([])


def delete_totp_device(request, device_id):
    totp_device = get_object_or_404(TOTPDevice, id=device_id)

    # Check (for security purposes)
    if request.user == totp_device.user:
        if request.method == 'POST':
            totp_device.delete()
            # return all user devices
            return view_totp_devices(request)

    return totp_device
