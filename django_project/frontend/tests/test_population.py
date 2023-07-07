from django.test import TestCase
from django.urls import reverse
from frontend.tests.model_factories import UserF
from stakeholder.models import (
    OrganisationUser
)
from stakeholder.factories import (
    organisationFactory
)
from frontend.tests.request_factories import OrganisationAPIRequestFactory
from frontend.api_views.population import (
    PopulationMetadataList,
    UploadPopulationAPIVIew
)
from property.factories import (
    PropertyFactory
)
from species.factories import (
    TaxonF,
    ManagementStatusFactory
)
from population_data.factories import (
    NatureOfPopulationFactory
)
from population_data.models import (
    Month,
    AnnualPopulation,
    AnnualPopulationPerActivity
)
from species.models import OwnedSpecies


class TestPopulationAPIViews(TestCase):
    fixtures = [
        'open_close_systems.json',
        'count_method.json',
        'survey_methods.json',
        'sampling_size_units.json',
        'activity_type.json'
    ]

    def setUp(self) -> None:
        # insert organisation
        self.organisation = organisationFactory.create()
        self.factory = OrganisationAPIRequestFactory(self.organisation)
        self.user_1 = UserF.create(username='test_1')
        OrganisationUser.objects.create(
            user=self.user_1,
            organisation=self.organisation
        )
        self.month = Month.objects.create(
            name='July',
            sort_order=7
        )
        ManagementStatusFactory.create()
        NatureOfPopulationFactory.create()
    
    def test_get_metadata_list(self):
        request = self.factory.get(
            reverse('population-metadata')
        )
        request.user = self.user_1
        view = PopulationMetadataList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_upload_population_data(self):
        property = PropertyFactory.create(
            organisation=self.organisation
        )
        taxon = TaxonF.create()
        data = {
            'taxon_id': taxon.id,
            'year': 2023,
            'property_id': property.id,
            'month': 7,
            'annual_population': {
                'present': True,
                'total': 20,
                'adult_male': 5,
                'adult_female': 7,
                'sub_adult_male': 8,
                'group': 1,
                'open_close_id': 1,
                'area_available_to_species': 5.5,
                'count_method_id': 1,
                'survey_method_id': 1,
                'sampling_effort': 1.25,
                'sampling_size_unit_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes'
            },
            'intake_population': {
                'activity_type_id': 1,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            },
            'offtake_population': {
                'activity_type_id': 2,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is intake notes'
            }
        }
        kwargs = {
            'property_id': property.id
        }
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
        # assert owned species
        owned_species = OwnedSpecies.objects.filter(
            taxon=taxon,
            property=property
        ).first()
        self.assertTrue(owned_species)
        # assert annual population data
        annual_population = AnnualPopulation.objects.filter(
            owned_species=owned_species,
            year=2023
        ).first()
        self.assertTrue(annual_population)
        # assert annual population per activity - intake
        annual_intake = AnnualPopulationPerActivity.objects.filter(
            owned_species=owned_species,
            year=2023,
            activity_type_id=1
        ).first()
        self.assertTrue(annual_intake)
        # assert annual population per activity - offtake
        annual_offtake = AnnualPopulationPerActivity.objects.filter(
            owned_species=owned_species,
            year=2023,
            activity_type_id=2
        ).first()
        self.assertTrue(annual_offtake)
