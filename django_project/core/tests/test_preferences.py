from django.test import TestCase, override_settings, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from core.models.preferences import SitePreferences


User = get_user_model()
MOCKED_INSTALLED_APPS = tuple(x for x in settings.INSTALLED_APPS if x != 'easyaudit')


class SitePreferencesTest(TestCase):
    """SitePreferences test case."""

    def setUp(self) -> None:
        self.superuser = User.objects.create(
            username='superuser',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        TOTPDevice.objects.create(
            user=self.superuser, name='Test Device', confirmed=True)

    def test_site_preferences(self):
        preferences = SitePreferences.preferences()
        preferences.property_overlaps_threshold = None
        preferences.save()
        self.assertFalse(preferences.property_overlaps_threshold)
        # test delete do nothing
        preferences.delete()
        self.assertTrue(SitePreferences.objects.filter(pk=1).exists())

    def test_site_preferences_admin_site_list(self):
        client = Client()
        client.force_login(self.superuser)
        response = client.get(
            reverse('admin:core_sitepreferences_changelist'))
        self.assertEqual(response.status_code, 302)
        response = client.get(
            reverse('admin:core_sitepreferences_changelist'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Threshold for checking overlaps between properties')


@override_settings(INSTALLED_APPS=MOCKED_INSTALLED_APPS)
class MockedSitePreferencesTest(TestCase):
    """Mocked migration without easyaudit."""
    
    def test_migrate_site_preferences(self):
        preferences = SitePreferences.preferences()
        self.assertTrue(preferences)
