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
    StatisticalModelOutputF,
    SpeciesModelOutputF
)
from frontend.models import SPECIES_PER_PROPERTY
from frontend.models.base_task import DONE
from frontend.api_views.statistical import SpeciesTrend
from species.factories import (
    TaxonRankFactory
)
from species.models import Taxon, TaxonRank
from population_data.factories import AnnualPopulationF
from property.factories import PropertyFactory
from occurrence.models import SurveyMethod

def mocked_cache_get(self, *args, **kwargs):
    return OrderedDict({
        'test': '12345'
    })

def mocked_cache_get_empty(self, *args, **kwargs):
    return None

def mocked_clear_cache(self, *args, **kwargs):
    return 1

class TestSpeciesTrend(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_1 = UserF.create(
            username='testuserd',
            password="testpassword"
        )
        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

        self.taxon = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_verbatim="Lion",
            scientific_name = "Penthera leo"
        )

        self.taxon1 = Taxon.objects.create(
            taxon_rank=taxon_rank, common_name_verbatim="Cheetah",
            scientific_name = "Cheetah"
        )

        # Create test data, including properties and owned species
        self.property1 = PropertyFactory.create(
            name="Property 1"
        )

        survey_method = SurveyMethod.objects.create(
            name='test_survey'
        )

        self.annual_population = AnnualPopulationF.create(
            year=2020,
            property=self.property1,
            user=self.user_1,
            taxon=self.taxon,
            total=100,
            adult_male=10,
            adult_female=10,
            juvenile_male=10,
            juvenile_female=10,
            sub_adult_total=10,
            sub_adult_male=10,
            sub_adult_female=10,
            juvenile_total=10,
            survey_method=survey_method
        )
    
    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get))
    def test_species_trend_from_cache(self):
        SpeciesModelOutputF.create(
            taxon=self.taxon,
            is_latest=True,
            status=DONE
        )
        url = reverse('species-population-trend')
        url += f'?species={self.annual_population.taxon.scientific_name}'
        request = self.factory.get(url)
        
        request.user = UserF.create()
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('test', response.data)
        self.assertEqual(response.data['test'], '12345')

    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get_empty))
    def test_species_trend_without_cache(self):
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
            type=SPECIES_PER_PROPERTY
        )
        url = reverse('species-population-trend')
        url += f'?species={self.annual_population.taxon.scientific_name}'
        request = self.factory.get(url)
        request.user = UserF.create()
        view = SpeciesTrend.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
