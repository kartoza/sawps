from django.test import TestCase
from django.urls import reverse
from uuid import uuid4
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
    UploadPopulationAPIVIew,
    FetchDraftPopulationUpload,
    DraftPopulationUpload,
    FetchPopulationData,
    CanWritePopulationData
)
from property.factories import (
    PropertyFactory,
    ProvinceFactory
)
from species.factories import TaxonF

from population_data.models import (
    AnnualPopulation,
    AnnualPopulationPerActivity,
    PopulationStatus,
    PopulationEstimateCategory,
    SamplingEffortCoverage
)
from population_data.factories import (
    CertaintyF,
    AnnualPopulationF
)


def mocked_clear_cache(self, *args, **kwargs):
    return 1


class TestPopulationAPIViews(TestCase):
    fixtures = [
        'open_close_systems.json',
        'survey_methods.json',
        'sampling_size_units.json',
        'activity_type.json'
    ]

    def setUp(self) -> None:
        # insert organisation
        self.organisation = organisationFactory.create()
        self.factory = OrganisationAPIRequestFactory(self.organisation)
        self.user_1 = UserF.create(username='test_1')
        self.superuser = UserF.create(
            username='superuser', is_superuser=True,
            is_staff=True, is_active=True)
        OrganisationUser.objects.create(
            user=self.user_1,
            organisation=self.organisation
        )
        self.population_status = PopulationStatus.objects.create(
            name='Status 1'
        )
        self.estimate = PopulationEstimateCategory.objects.create(
            name='Estimate 1'
        )
        self.coverage = SamplingEffortCoverage.objects.create(
            name='Coverage 1'
        )
        self.certainty = CertaintyF.create(
            description='Certainty1',
            name='1'
        )
        self.province = ProvinceFactory(name='Western Cape')
        self.property_1 = PropertyFactory.create(
            organisation=self.organisation
        )
        self.taxon_1 = TaxonF.create()
        self.sample_data = {
            'taxon_id': self.taxon_1.id,
            'year': 2023,
            'property_id': self.property_1.id,
            'month': 7,
            'annual_population': {
                'present': True,
                'total': 20,
                'adult_male': 5,
                'adult_female': 7,
                'sub_adult_male': 8,
                'adult_total': 12,
                'sub_adult_total': 8,
                'juvenile_total': 0,
                'group': 1,
                'open_close_id': 1,
                'area_available_to_species': 5.5,
                'survey_method_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes',
                'sampling_effort_coverage_id': self.coverage.id,
                'population_status_id': self.population_status.id,
                'population_estimate_category_id': self.estimate.id
            },
            'intake_populations': [{
                'activity_type_id': 1,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            },
            {
                'activity_type_id': 100,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            }],
            'offtake_populations': [{
                'activity_type_id': 2,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 100,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 3,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is invalid notes'
            }]
        }

    def test_get_metadata_list(self):
        request = self.factory.get(
            reverse('population-metadata')
        )
        request.user = self.user_1
        view = PopulationMetadataList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.data.keys()),
            [
                'taxons',
                'survey_methods',
                'intake_events',
                'offtake_events',
                'sampling_effort_coverages',
                'population_statuses',
                'population_estimate_categories'
            ]
        )

    def test_can_add_new_population_data(self):
        # superuser should be allowed
        kwargs = {
            'property_id': self.property_1.id
        }
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=self.sample_data, format='json'
        )
        request.user = self.superuser
        view = CanWritePopulationData.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'OK')
        # user_2 should not be allowed
        user_2 = UserF.create(username='user_2')
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=self.sample_data, format='json'
        )
        request.user = user_2
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'],
                         CanWritePopulationData.ADD_DATA_NO_PERMISSION_MESSAGE)
        # user_1 should be allowed
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=self.sample_data, format='json'
        )
        request.user = self.user_1
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'OK')

    def test_can_overwrite_population_data(self):
        user_2 = UserF.create(username='user_2')
        population_1 = AnnualPopulationF(
            total=120,
            adult_male=19,
            adult_female=100,
            adult_total=119,
            year=self.sample_data['year'],
            user=self.user_1,
            property=self.property_1,
            taxon=self.taxon_1
        )
        kwargs = {
            'property_id': self.property_1.id
        }
        # case - user is not the owner/manager
        data = self.sample_data
        data['id'] = population_1.id
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = user_2
        view = CanWritePopulationData.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], CanWritePopulationData.EDIT_DATA_NO_PERMISSION_MESSAGE)
        # case - add new data to existing year - user is not allowed to overwrite other data
        data['id'] = 0
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = user_2
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'],
                         CanWritePopulationData.EDIT_DATA_NO_PERMISSION_OVERWRITE_MESSAGE.format(data['year']))
        # case - add new data to existing year - user is allowed to overwrite other data
        data['id'] = 0
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'],
                         CanWritePopulationData.EDIT_DATA_CONFIRM_OVERWRITE_MESSAGE.format(data['year']))
        self.assertEqual(response.data['other_id'], population_1.id)
        # case - change year of existing data - user is allowed to overwrite other data
        data['id'] = population_1.id
        data['year'] = 2020
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'OK')
        # case - change year of existing data - user is allowed to overwrite other data
        # the updated year has already data
        population_2 = AnnualPopulationF(
            total=99,
            year=data['year'],
            user=self.user_1,
            property=self.property_1,
            taxon=self.taxon_1
        )
        request = self.factory.post(
            reverse('can-upload-population-data', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'],
                         CanWritePopulationData.EDIT_DATA_CONFIRM_OVERWRITE_MESSAGE.format(data['year']))
        self.assertEqual(response.data['other_id'], population_2.id)

    def test_upload_population_data(self):
        user_2 = UserF.create(username='user_2')
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
                'adult_total': 12,
                'sub_adult_total': 8,
                'juvenile_total': 0,
                'group': 1,
                'open_close_id': 1,
                'area_available_to_species': 5.5,
                'survey_method_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes',
                'sampling_effort_coverage_id': self.coverage.id,
                'population_status_id': self.population_status.id,
                'population_estimate_category_id': self.estimate.id
            },
            'intake_populations': [{
                'activity_type_id': 1,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            },
            {
                'activity_type_id': 100,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            }],
            'offtake_populations': [{
                'activity_type_id': 2,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 100,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 3,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is invalid notes'
            }]
        }
        kwargs = {
            'property_id': property.id
        }
        # test with user non-organisation, should return 403
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = user_2
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 403)
        # test with user that belongs to property organisation
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
        # assert annual population data
        annual_population = AnnualPopulation.objects.filter(
            taxon=taxon,
            property=property,
            year=2023
        ).first()
        self.assertTrue(annual_population)
        self.assertEqual(annual_population.area_available_to_species, 5.5)
        self.assertEqual(annual_population.total, data['annual_population']['total'])
        self.assertEqual(annual_population.adult_total, data['annual_population']['adult_total'])
        self.assertEqual(annual_population.sub_adult_total, data['annual_population']['sub_adult_total'])
        self.assertEqual(annual_population.juvenile_total, data['annual_population']['juvenile_total'])
        # assert annual population per activity - intake
        annual_intake = AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population,
            year=2023,
            activity_type_id=1
        ).first()
        self.assertTrue(annual_intake)
        # assert annual population per activity - offtake
        annual_offtake = AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population,
            year=2023,
            activity_type_id=2
        ).first()
        self.assertTrue(annual_offtake)
        # test fetch the annual population data
        fetch_kwargs = {
            'id': annual_population.id
        }
        request = self.factory.get(
            reverse('fetch-population-data', kwargs=fetch_kwargs)
        )
        request.user = self.user_1
        view = FetchPopulationData.as_view()
        response = view(request, **fetch_kwargs)
        self.assertEqual(response.status_code, 200)
        # test to update and overwrite the data
        data = {
            'taxon_id': taxon.id,
            'year': 2023,
            'property_id': property.id,
            'month': 7,
            'annual_population': {
                'present': True,
                'total': 45,
                'adult_male': 0,
                'adult_female': 0,
                'sub_adult_male': 0,
                'adult_total': 0,
                'sub_adult_total': 0,
                'juvenile_total': 0,
                'group': 1,
                'open_close_id': 1,
                'area_available_to_species': 5.5,
                'survey_method_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes',
                'sampling_effort_coverage_id': self.coverage.id,
                'population_status_id': self.population_status.id,
                'population_estimate_category_id': self.estimate.id
            },
            'intake_populations': [],
            'offtake_populations': []
        }
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Please confirm to overwrite data at year 2023')
        data['confirm_overwrite'] = True
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
        annual_population.refresh_from_db()
        self.assertEqual(annual_population.total, data['annual_population']['total'])
        self.assertEqual(annual_population.adult_total, data['annual_population']['adult_male'])
        self.assertEqual(annual_population.adult_total, data['annual_population']['adult_female'])
        self.assertEqual(annual_population.adult_total, data['annual_population']['adult_total'])
        self.assertEqual(annual_population.adult_total, data['annual_population']['sub_adult_male'])
        self.assertEqual(annual_population.sub_adult_total, data['annual_population']['sub_adult_total'])
        self.assertEqual(annual_population.juvenile_total, data['annual_population']['juvenile_total'])
        self.assertFalse(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population,
            year=2023,
            activity_type_id=1
        ).exists())
        self.assertFalse(AnnualPopulationPerActivity.objects.filter(
            annual_population=annual_population,
            year=2023,
            activity_type_id=2
        ))
        # test overwrite other year data - not allowed using user_1
        OrganisationUser.objects.create(
            user=user_2,
            organisation=self.organisation
        )
        population_2 = AnnualPopulationF(
            total=99,
            year=2010,
            user=user_2,
            property=annual_population.property,
            taxon=annual_population.taxon
        )
        data['id'] = annual_population.id
        data['year'] = population_2.year
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 403)
        # test overwrite other year data - allowed using superuser
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs) + f'?uuid={str(uuid4())}',
            data=data, format='json'
        )
        request.user = self.superuser
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
        annual_population.refresh_from_db()
        self.assertEqual(annual_population.year, population_2.year)
        self.assertEqual(annual_population.total, data['annual_population']['total'])
        self.assertFalse(AnnualPopulation.objects.filter(id=population_2.id).exists())

    def test_upload_population_data_future_year(self):
        property = PropertyFactory.create(
            organisation=self.organisation
        )
        taxon = TaxonF.create()
        data = {
            'taxon_id': taxon.id,
            'year': 2080,
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
                'survey_method_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes',
                'sampling_effort_coverage_id': self.coverage.id,
                'population_status_id': self.population_status.id,
                'population_estimate_category_id': self.estimate.id
            },
            'intake_populations': [{
                'activity_type_id': 1,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            },
            {
                'activity_type_id': 100,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            }],
            'offtake_populations': [{
                'activity_type_id': 2,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 100,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is invalid notes'
            },
            {
                'activity_type_id': 3,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is invalid notes'
            }]
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
        self.assertEqual(
            response.status_code, 400
        )
        self.assertEqual(
            response.data,
            {'detail': 'Year should not exceed current year!'}
        )

    def test_save_draft(self):
        # save draft
        property = PropertyFactory.create(
            organisation=self.organisation
        )
        taxon = TaxonF.create()
        form_data = {
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
                'survey_method_id': 1,
                'area_covered': 1.2,
                'note': 'This is notes'
            },
            'intake_populations': [{
                'activity_type_id': 1,
                'total': 12,
                'adult_male': 5,
                'adult_female': 7,
                'founder_population': True,
                'reintroduction_source': 'Source A',
                'permit': 900,
                'note': 'This is intake notes'
            }],
            'offtake_populations': [{
                'activity_type_id': 2,
                'total': 6,
                'adult_male': 4,
                'adult_female': 2,
                'translocation_destination': 'Dest A',
                'permit': 900,
                'note': 'This is intake notes'
            }]
        }
        kwargs = {
            'property_id': property.id
        }
        request = self.factory.post(
            reverse('draft-upload-species', kwargs=kwargs),
            data={
                'name': 'save draft test',
                'last_step': 1,
                'form_data': form_data
            },
            format='json'
        )
        request.user = self.user_1
        view = DraftPopulationUpload.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 201)
        self.assertIn('uuid', response.data)
        draft_uuid = response.data['uuid']
        # fetch draft
        kwargs = {
            'draft_uuid': draft_uuid
        }
        request = self.factory.get(
            reverse('fetch-draft-upload-species', kwargs=kwargs)
        )
        request.user = self.user_1
        view = FetchDraftPopulationUpload.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        # fetch list of draft
        kwargs = {
            'property_id': property.id
        }
        request = self.factory.get(
            reverse('draft-upload-species', kwargs=kwargs)
        )
        request.user = self.user_1
        view = DraftPopulationUpload.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        # delete draft
        kwargs = {
            'draft_uuid': draft_uuid
        }
        request = self.factory.delete(
            reverse('fetch-draft-upload-species', kwargs=kwargs)
        )
        request.user = self.user_1
        view = FetchDraftPopulationUpload.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)

    def test_fetch_non_existing_population_data(self):
        kwargs = {
            'id': 1000
        }
        request = self.factory.get(
            reverse('fetch-population-data', kwargs=kwargs)
        )
        request.user = self.user_1
        view = FetchPopulationData.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 404)
