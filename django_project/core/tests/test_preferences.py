from django.test import TestCase, override_settings
from django.conf import settings
from core.models.preferences import SitePreferences


MOCKED_INSTALLED_APPS = tuple(x for x in settings.INSTALLED_APPS if x != 'easyaudit')


class SitePreferencesTest(TestCase):
    """SitePreferences test case."""

    def test_site_preferences(self):
        preferences = SitePreferences.preferences()
        preferences.property_overlaps_threshold = None
        preferences.save()
        self.assertFalse(preferences.property_overlaps_threshold)
        # test delete do nothing
        preferences.delete()
        self.assertTrue(SitePreferences.objects.filter(pk=1).exists())

    @override_settings(INSTALLED_APPS=MOCKED_INSTALLED_APPS)
    def test_migrate_site_preferences(self):
        preferences = SitePreferences.preferences()
        self.assertTrue(preferences)
