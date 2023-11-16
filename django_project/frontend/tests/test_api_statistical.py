from django.test import TestCase
from django.urls import reverse
from collections import OrderedDict
import mock
from rest_framework.test import APIRequestFactory
from frontend.tests.model_factories import UserF
from species.factories import TaxonF
from frontend.tests.model_factories import (
    StatisticalModelF,
    StatisticalModelOutputF,
    SpeciesModelOutputF
)
from frontend.models.statistical import NATIONAL_TREND
from frontend.api_views.statistical import SpeciesNationalTrend
from frontend.models.base_task import DONE


def mocked_cache_get(self, *args, **kwargs):
    return OrderedDict({
        'test': '12345'
    })


def mocked_cache_get_empty(self, *args, **kwargs):
    return None


def mocked_clear_cache(self, *args, **kwargs):
    return 1


class TestAPIStatistical(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(username='test_1')
        self.taxon = TaxonF.create()
    
    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get))
    def test_national_trend_from_cache(self):
        SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=True,
            status=DONE
        )
        kwargs = {
            'species_id': self.taxon.id
        }
        request = self.factory.get(
            reverse('species-national-trend', kwargs=kwargs)
        )
        request.user = UserF.create()
        view = SpeciesNationalTrend.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn('test', response.data)
        self.assertEqual(response.data['test'], '12345')

    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get_empty))
    def test_national_trend_without_cache(self):
        SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=True,
            status=DONE
        )
        model = StatisticalModelF.create(
            taxon=self.taxon
        )
        StatisticalModelOutputF.create(
            model=model,
            type=NATIONAL_TREND
        )
        kwargs = {
            'species_id': self.taxon.id
        }
        request = self.factory.get(
            reverse('species-national-trend', kwargs=kwargs)
        )
        request.user = UserF.create()
        view = SpeciesNationalTrend.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
