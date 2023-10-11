from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status


class TestOrganisationAPIView(TestCase):
    fixtures = [
        'activity_type.json'
    ]

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        device = TOTPDevice(
            user=self.user,
            name='device_name'
        )
        device.save()
        self.client.login(username='testuser', password='testpassword')

    def test_list_activity_types(self):
        url = reverse('activity-type')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            {
                "id": 1,
                "name": "Other",
                "recruitment": None,
                "colour": None,
                "export_fields": [],
            },
            {
                "id": 3,
                "name": "Planned Euthanasia/DCA",
                "recruitment": None,
                "colour": None,
                "export_fields": ["intake_permit"],
            },
            {
                "id": 4,
                "name": "Planned Hunt/Cull",
                "recruitment": None,
                "colour": None,
                "export_fields": ["intake_permit"],
            },
            {
                "id": 5,
                "name": "Translocation (Intake)",
                "recruitment": None,
                "colour": None,
                "export_fields": [
                    "intake_permit",
                    "translocation_destination",
                    "offtake_permit",
                ],
            },
            {
                "id": 6,
                "name": "Translocation (Offtake)",
                "recruitment": None,
                "colour": None,
                "export_fields": [
                    "translocation_destination",
                    "founder_population",
                    "reintroduction_source",
                ],
            },
            {
                "id": 2,
                "name": "Unplanned/Illegal Hunting",
                "recruitment": None,
                "colour": None,
                "export_fields": [],
            },
        ]

        self.assertEqual(response.json(), expected_response)
