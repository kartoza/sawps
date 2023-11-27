from django.test import TestCase
from django.urls import reverse
from collections import OrderedDict
import mock
import json
from rest_framework.test import APIRequestFactory
from django.core.files.base import ContentFile
from frontend.tests.model_factories import UserF
from property.factories import PropertyFactory
from species.factories import TaxonF
from frontend.tests.model_factories import (
    StatisticalModelF,
    StatisticalModelOutputF,
    SpeciesModelOutputF
)
from frontend.models.statistical import NATIONAL_TREND
from frontend.api_views.statistical import (
    SpeciesNationalTrend,
    SpeciesTrend,
    DownloadTrendDataAsJson
)
from frontend.models.base_task import DONE


def mocked_property_trend():
    return OrderedDict({
        "property_trend": [
            {
                "property": "Test Reserve",
                "year": 2002,
                "fitted_pop_est": 12.21,
                "se.fit": 2.1,
                "lower_ci": 8.01,
                "upper_ci": 16.42,
                "species": "Loxodonta africana",
                "province": "Limpopo",
                "ownership": "Private",
                "open_closed": "Closed",
                "raw_pop_est": 17,
                "survey_method": "Aerial census total count helicopter",
                "property_size_ha": 18782,
                "area_available_to_species": 16000,
                "yr_min": 2002,
                "yr_max": 2021,
                "range_yrs": 19,
                "yrs_data": 8,
                "most_recent_fitted_pop_est": 27.01,
                "most_recent_raw_pop_est": 25,
                "pop_size_cat": "medium"
            }
        ]
    })


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
        request.user = self.user_1
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
        request.user = self.user_1
        view = SpeciesNationalTrend.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    @mock.patch('django.core.cache.cache.get')
    def test_species_trend(self, mocked_cache):
        # get invalid type
        output = SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=True,
            status=DONE
        )
        url = reverse('species-population-trend')
        url += f'?species={self.taxon.scientific_name}&level=national&data_type=abcdef'
        request = self.factory.get(url)
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        # get without model output
        output.is_latest = False
        output.save()
        url = reverse('species-population-trend')
        url += f'?species={self.taxon.scientific_name}&level=provincial&data_type=trend'
        request = self.factory.get(url)
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # get national growth empty output file
        output.is_latest = True
        output.save()
        mocked_cache.side_effect = mocked_cache_get_empty
        url = reverse('species-population-trend')
        url += f'?species={self.taxon.scientific_name}&level=national&data_type=growth'
        request = self.factory.get(url)
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # get provincial growth
        mocked_cache.side_effect = mocked_cache_get
        url = reverse('species-population-trend')
        url += f'?species={self.taxon.scientific_name}&level=provincial&data_type=growth'
        request = self.factory.get(url)
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_species_property_trend(self):
        property = PropertyFactory.create(
            name='Test Reserve'
        )
        output = SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=False,
            status=DONE,
            output_file=None
        )
        data = {
            'species': self.taxon.scientific_name,
            'property': str(property.id)
        }
        # empty output_file test
        request = self.factory.post(
            reverse('species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # empty file
        output.output_file = None
        output.is_latest = True
        output.save()
        request = self.factory.post(
            reverse('species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # has file
        output.output_file.save('test.json', ContentFile(json.dumps(mocked_property_trend())))
        request = self.factory.post(
            reverse('species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # test empty property id
        data = {
            'species': self.taxon.scientific_name,
            'property': ''
        }
        request = self.factory.post(
            reverse('species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # remove test file
        output.delete()

    def test_download_trend_json(self):
        property = PropertyFactory.create(
            name='Test Reserve'
        )
        output = SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=False,
            status=DONE,
            output_file=None
        )
        data = {
            'species': self.taxon.scientific_name,
            'property': str(property.id)
        }
        # empty output_file test
        request = self.factory.post(
            reverse('download-species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = DownloadTrendDataAsJson.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)
        # has file
        output.is_latest = True
        output.output_file.save('test.json', ContentFile(json.dumps(mocked_property_trend())))
        request = self.factory.post(
            reverse('download-species-population-trend'),
            data=data, format='json'
        )
        request.user = self.user_1
        view = DownloadTrendDataAsJson.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertEqual(response.get('Content-Type'), 'application/json')
        # remove test file
        output.delete()
