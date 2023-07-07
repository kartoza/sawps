from django.test import TestCase
from django.urls import reverse
from frontend.tests.model_factories import UserF
from stakeholder.factories import (
    organisationFactory
)
from frontend.tests.request_factories import OrganisationAPIRequestFactory
from frontend.api_views.population import (
    PopulationMetadataList,
    UploadPopulationAPIVIew
)


class TestPopulationAPIViews(TestCase):

    def setUp(self) -> None:
        # insert organisation
        self.organisation = organisationFactory.create()
        self.factory = OrganisationAPIRequestFactory(self.organisation)
        self.user_1 = UserF.create(username='test_1')
    
    def test_get_metadata_list(self):
        request = self.factory.get(
            reverse('population-metadata')
        )
        request.user = self.user_1
        view = PopulationMetadataList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_upload_population_data(self):
        data = {}
        kwargs = {
            'property_id': 1
        }
        request = self.factory.post(
            reverse('population-upload', kwargs=kwargs),
            data=data, format='json'
        )
        request.user = self.user_1
        view = UploadPopulationAPIVIew.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 204)
