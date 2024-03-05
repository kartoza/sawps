import json
import mock
from django.utils import timezone
from rest_framework import status
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.test import TestCase, Client
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from core.settings.utils import absolute_path
from frontend.tests.model_factories import UserF
from property.models import PropertyOverlaps
from property.factories import ProvinceFactory, PropertyFactory
from stakeholder.factories import organisationFactory
from property.tasks.check_overlaps import (
    OverlapItem,
    check_for_resolved_overlaps,
    check_overlaps_in_properties,
    property_check_overlaps_each_other
)
from core.models.preferences import SitePreferences


def mocked_process(*args, **kwargs):
    return 1


class TestCheckOverlaps(TestCase):

    def setUp(self):
        self.superuser = UserF.create(
            username='superuser', is_superuser=True,
            is_staff=True, is_active=True)
        TOTPDevice.objects.create(
            user=self.superuser, name='Test Device', confirmed=True)
        geom_path = absolute_path(
            'frontend', 'tests',
            'geojson', 'property_geom_1.geojson')
        with open(geom_path) as geojson:
            data = json.load(geojson)
            geom_str = json.dumps(data['features'][0]['geometry'])
            self.geom_1 = GEOSGeometry(geom_str, srid=4326)
        geom_path = absolute_path(
            'frontend', 'tests',
            'geojson', 'geom_poly.geojson')
        with open(geom_path) as geojson:
            data = json.load(geojson)
            geom_poly_str = json.dumps(data['features'][0]['geometry'])
            self.geom_2 = GEOSGeometry(geom_poly_str, srid=4326)
        self.province = ProvinceFactory(name='Western Cape')
        self.organisation = organisationFactory(name='CapeNature')
        self.property_1 = PropertyFactory(
            name='Lupin',
            province=self.province,
            organisation=self.organisation,
            created_by=self.superuser
        )
        self.property_2 = PropertyFactory(
            name='Lupin_2',
            province=self.province,
            organisation=self.organisation,
            created_by=self.superuser
        )

    def test_create_overlap_item(self):
        item = OverlapItem(1, 2, self.geom_1)
        self.assertTrue(isinstance(item.intersect_geom, MultiPolygon))
        self.assertTrue(item.overlap_area_size > 0)
        self.assertTrue(item.is_new())
        self.assertFalse(item.get_existing())
        item = OverlapItem(1, 2, self.geom_2)
        self.assertTrue(isinstance(item.intersect_geom, MultiPolygon))
        self.assertTrue(item.overlap_area_size > 0)
        self.assertTrue(item.is_new())
        self.assertFalse(item.get_existing())

    def test_check_for_overlap_size(self):
        item = OverlapItem(1, 2, self.geom_1)
        self.assertTrue(isinstance(item.intersect_geom, MultiPolygon))
        self.assertTrue(item.overlap_area_size > 0)
        # test with empty threshold
        preferences = SitePreferences.preferences()
        preferences.property_overlaps_threshold = None
        preferences.save()
        self.assertTrue(item.check_for_overlap_size())
        # test with upper threshold
        preferences = SitePreferences.preferences()
        preferences.property_overlaps_threshold = item.overlap_area_size + 1
        preferences.save()
        self.assertFalse(item.check_for_overlap_size())

    def load_test_geom_to_properties(self, geom_path):
        with open(geom_path) as geojson:
            data = json.load(geojson)
            geom_str = json.dumps(data['features'][0]['geometry'])
            self.property_1.geometry = GEOSGeometry(geom_str, srid=4326)
            self.property_1.save()
            geom_str = json.dumps(data['features'][1]['geometry'])
            self.property_2.geometry = GEOSGeometry(geom_str, srid=4326)
            self.property_2.save()

    def test_check_overlaps_in_properties(self):
        # case: no overlaps
        geom_path = absolute_path(
            'property', 'tests',
            'geojson', 'geom_no_overlaps.geojson')
        self.load_test_geom_to_properties(geom_path)
        results = check_overlaps_in_properties()
        self.assertEqual(len(results), 0)
        # case: overlaps
        geom_path = absolute_path(
            'property', 'tests',
            'geojson', 'geom_overlaps.geojson')
        self.load_test_geom_to_properties(geom_path)
        results = check_overlaps_in_properties()
        self.assertEqual(len(results), 1)
        # case: within
        geom_path = absolute_path(
            'property', 'tests',
            'geojson', 'geom_within.geojson')
        self.load_test_geom_to_properties(geom_path)
        results = check_overlaps_in_properties()
        self.assertEqual(len(results), 1)

    def test_check_for_resolved_overlaps(self):
        overlaps = PropertyOverlaps.objects.create(
            property=self.property_1,
            other=self.property_2,
            reported_at=timezone.now(),
            resolved=False
        )
        overlaps_list = [
            OverlapItem(99, 98, self.geom_1)
        ]
        result = check_for_resolved_overlaps(overlaps_list)
        self.assertEqual(result, 1)
        overlaps.refresh_from_db()
        self.assertTrue(overlaps.resolved)
        self.assertTrue(overlaps.resolved_at)

    def test_property_check_overlaps_each_other(self):
        # new overlaps 1, resolved 1
        property_3 = PropertyFactory(
            name='Test3',
            province=self.province,
            organisation=self.organisation,
            created_by=self.superuser,
            geometry=None
        )
        property_4 = PropertyFactory(
            name='Test4',
            province=self.province,
            organisation=self.organisation,
            created_by=self.superuser,
            geometry=None
        )
        overlaps = PropertyOverlaps.objects.create(
            property=property_3,
            other=property_4,
            reported_at=timezone.now(),
            resolved=False
        )
        geom_path = absolute_path(
            'property', 'tests',
            'geojson', 'geom_overlaps.geojson')
        self.load_test_geom_to_properties(geom_path)
        new_overlap, resolved = property_check_overlaps_each_other()
        self.assertEqual(new_overlap, 1)
        self.assertEqual(resolved, 1)
        overlaps.refresh_from_db()
        self.assertTrue(overlaps.resolved)
        # case: resolved overlaps become overlap again
        PropertyOverlaps.objects.all().delete()
        overlaps = PropertyOverlaps.objects.create(
            property=property_3,
            other=property_4,
            reported_at=timezone.now(),
            resolved=False
        )
        overlaps_resolved = PropertyOverlaps.objects.create(
            property=self.property_1,
            other=self.property_2,
            reported_at=timezone.now(),
            resolved=True
        )
        new_overlap, resolved = property_check_overlaps_each_other()
        self.assertEqual(new_overlap, 1)
        self.assertEqual(resolved, 1)
        overlaps.refresh_from_db()
        self.assertTrue(overlaps.resolved)
        overlaps_resolved.refresh_from_db()
        self.assertFalse(overlaps_resolved.resolved)

    def test_admin_overlaps_list(self):
        overlaps = PropertyOverlaps.objects.create(
            property=self.property_1,
            other=self.property_2,
            overlap_area_size=100,
            reported_at=timezone.now(),
            resolved=False
        )
        PropertyOverlaps.objects.create(
            property=self.property_1,
            other=self.property_2,
            overlap_area_size=10000,
            reported_at=timezone.now(),
            resolved=False
        )
        client = Client()
        client.force_login(self.superuser)
        response = client.get(
            reverse('admin:property_propertyoverlaps_changelist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Lupin_2')
        self.assertContains(response, '100.00 sqm')
        self.assertContains(response, '1.00 ha')
        response = client.post(
            reverse('admin:property_propertyoverlaps_changelist'),
            {
                'action': 'resolve_overlaps',
                '_selected_action': [overlaps.id]
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        overlaps.refresh_from_db()
        self.assertTrue(overlaps.resolved)        

    @mock.patch('property.tasks.check_overlaps.'
                'property_check_overlaps_each_other.delay')
    def test_admin_property_trigger_check_overlaps(self, mocked_task):
        mocked_task.side_effect = mocked_process
        client = Client()
        client.force_login(self.superuser)
        response = client.post(
            reverse('admin:property_property_changelist'),
            {
                'action': 'run_check_overlaps',
                '_selected_action': [self.property_1.id]
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mocked_task.assert_called_once()

    @mock.patch('property.tasks.check_overlaps.area')
    def test_check_overlaps_ignored(self, mocked_area):
        mocked_area.return_value = 0.001
        # case: overlaps
        geom_path = absolute_path(
            'property', 'tests',
            'geojson', 'geom_overlaps.geojson')
        self.load_test_geom_to_properties(geom_path)
        results = check_overlaps_in_properties()
        mocked_area.assert_called_once()
        self.assertEqual(len(results), 0)
        # should return 0
        mocked_area.reset_mock()
        mocked_area.return_value = 1
        results = check_overlaps_in_properties()
        mocked_area.assert_called_once()
        self.assertEqual(len(results), 0)
        # should return 1
        mocked_area.reset_mock()
        mocked_area.return_value = 1.5
        results = check_overlaps_in_properties()
        mocked_area.assert_called_once()
        self.assertEqual(len(results), 1)
