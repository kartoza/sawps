from django.test import TestCase
from django.urls import reverse
import requests_mock
from collections import OrderedDict
import mock
from rest_framework.test import APIRequestFactory
from frontend.tests.model_factories import UserF
from species.factories import TaxonF
from frontend.tests.model_factories import (
    StatisticalModelF,
    StatisticalModelOutputF
)
from frontend.models.statistical import NATIONAL_TREND
from frontend.utils.statistical_model import PLUMBER_PORT
from frontend.api_views.statistical import SpeciesNationalTrend


def mocked_cache_get(self, *args, **kwargs):
    return OrderedDict({
        'test': '12345'
    })


def mocked_cache_get_empty(self, *args, **kwargs):
    return None


def mocked_clear_cache(self, *args, **kwargs):
    pass


class TestAPIStatistical(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(username='test_1')
        self.taxon = TaxonF.create()
    
    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get))
    def test_national_trend_from_cache(self):
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

    @mock.patch(
        'frontend.utils.statistical_model.'
        'clear_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
    @mock.patch(
        'frontend.utils.statistical_model.'
        'save_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get_empty))
    def test_national_trend_without_cache(self):
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
        with requests_mock.Mocker() as m:
            json_response = {'national_trend': 'abcde'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/api_{model.id}',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            request.user = UserF.create()
            view = SpeciesNationalTrend.as_view()
            response = view(request, **kwargs)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, 'abcde')

    @mock.patch(
        'frontend.utils.statistical_model.'
        'clear_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
    @mock.patch(
        'frontend.utils.statistical_model.'
        'save_statistical_model_output_cache',
        mock.Mock(side_effect=mocked_clear_cache)
    )
    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get_empty))
    def test_national_trend_without_output(self):
        kwargs = {
            'species_id': self.taxon.id
        }
        request = self.factory.get(
            reverse('species-national-trend', kwargs=kwargs)
        )
        with requests_mock.Mocker() as m:
            # without national trend model, it will use generic model
            json_response = {'national_trend': 'qwerty'}
            m.post(
                f'http://plumber:{PLUMBER_PORT}/statistical/generic',
                json=json_response,
                headers={'Content-Type':'application/json'},
                status_code=200
            )
            request.user = UserF.create()
            view = SpeciesNationalTrend.as_view()
            response = view(request, **kwargs)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, 'qwerty')
