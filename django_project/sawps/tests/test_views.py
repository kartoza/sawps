from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestViews(TestCase):
    """Test utilities."""

    def test_healthcheck(self):
        response = self.client.get(
            reverse('healthz')
        )
        self.assertTrue(
            response.status_code,
            status.HTTP_200_OK
        )
