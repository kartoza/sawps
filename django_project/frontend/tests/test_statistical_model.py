import mock
from django.test import TestCase, override_settings
from django.test import Client
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from core.settings.utils import DJANGO_ROOT
from frontend.models.statistical import (
    StatisticalModel,
    OutputTypeCategoryIndex
)
from frontend.tests.model_factories import (
    StatisticalModelF,
    StatisticalModelOutputF
)


def mocked_clear_cache(self, *args, **kwargs):
    return 1


class DummyTask:
    def __init__(self, id):
        self.id = id


def mocked_process(*args, **kwargs):
    return DummyTask(1)


class StatisticalModelAdminTestCase(TestCase):
    """StatisticalModel admin test case."""

    @classmethod
    def setUpTestData(cls):
        cls.model = StatisticalModelF.create()
        cls.output = StatisticalModelOutputF.create(
            model=cls.model
        )
        cls.user = User.objects.create(
            username='admin123', is_superuser=True, is_staff=True,
            is_active=True)
        TOTPDevice.objects.create(
            user=cls.user, name='Test Device', confirmed=True)

    @mock.patch('frontend.tasks.start_plumber.'
                'start_plumber_process.apply_async',
                mock.Mock(side_effect=mocked_process))
    def test_statistical_model_listing(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(
            reverse('admin:frontend_statisticalmodel_changelist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Taxon')
        response = client.post(
            reverse('admin:frontend_statisticalmodel_changelist'),
            {
                'action': 'restart_plumber_process',
                '_selected_action': [self.model.id]
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response, 'Plumber process will be started in background')

    @mock.patch('frontend.tasks.start_plumber.'
                'start_plumber_process.apply_async',
                mock.Mock(side_effect=mocked_process))
    def test_statistical_model_delete(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(
            reverse('admin:frontend_statisticalmodel_delete', kwargs={
                'object_id': self.model.id
            }),
            {
                'post': 'yes'
            },
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(StatisticalModel.objects.filter(
            id=self.model.id).exists())

    @mock.patch('frontend.tasks.start_plumber.'
                'start_plumber_process.apply_async',
                mock.Mock(side_effect=mocked_process))
    def test_statistical_model_download_sample_csv(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(
            reverse('admin:frontend_statisticalmodel_change', kwargs={
                'object_id': self.model.id
            }),
            {
                'taxon': self.model.taxon.id,
                'name': self.model.name,
                'code': self.model.code,
                'statisticalmodeloutput_set-TOTAL_FORMS': 1,
                'statisticalmodeloutput_set-INITIAL_FORMS': 1,
                'statisticalmodeloutput_set-0-id': self.output.id,
                'statisticalmodeloutput_set-0-model': self.model.id,
                'statisticalmodeloutput_set-0-type': 'national_trend',
                '_download-data-template': 'Download Data Template'
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'text/csv')
        self.assertTrue(response.has_header('Content-Disposition'))

    @override_settings(FIXTURE_DIRS=[DJANGO_ROOT])
    def test_reload_fixtures_output_type_categories(self):
        OutputTypeCategoryIndex.objects.create(
            type='period',
            value='Steady Decrease',
            sort_index=1
        )
        self.assertTrue(OutputTypeCategoryIndex.objects.count() == 1)
        client = Client()
        client.force_login(self.user)
        response = client.get(
            reverse('admin:reload-category-index-fixtures'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(OutputTypeCategoryIndex.objects.count() == 1)
