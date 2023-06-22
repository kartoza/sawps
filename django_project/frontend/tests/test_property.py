import json
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse
from core.settings.utils import absolute_path
from property.models import (
    PropertyType,
    Property,
    Parcel
)
from property.factories import (
    OwnershipStatusFactory,
    ProvinceFactory,
    PropertyFactory
)
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory
)
from frontend.models.parcels import (
    Erf,
    Holding
)
from frontend.tests.model_factories import UserF
from frontend.api_views.property import (
    CreateNewProperty,
    PropertyMetadataList,
    PropertyList,
    UpdatePropertyInformation,
    UpdatePropertyBoundaries,
    PropertyDetail
)
from frontend.tests.request_factories import OrganisationAPIRequestFactory


class TestPropertyAPIViews(TestCase):
    fixtures = [
        'property_type.json',
        'parcel_types.json'
    ]

    def setUp(self) -> None:
        # insert organisation
        self.organisation = organisationFactory.create()
        self.factory = OrganisationAPIRequestFactory(self.organisation)
        self.user_1 = UserF.create(username='test_1')
        self.user_2 = UserF.create(username='test_2')
        # insert province
        self.ownership_status = OwnershipStatusFactory.create()
        # insert province
        self.province = ProvinceFactory.create()
        # insert geom 1 and 2
        geom_path = absolute_path(
            'frontend', 'tests',
            'geojson', 'geom_1.geojson')
        with open(geom_path) as geojson:
            data = json.load(geojson)
            geom_str = json.dumps(data['features'][1]['geometry'])
            self.erf_1 = Erf.objects.create(
                geom=GEOSGeometry(geom_str),
                cname='C1234ABC'
            )
            geom_str = json.dumps(data['features'][0]['geometry'])
            self.holding_1 = Holding.objects.create(
                geom=GEOSGeometry(geom_str),
                cname='C1235DEF'
            )

    def test_create_new_property(self):
        property_type = PropertyType.objects.all().first()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'province_id': self.province.id,
            'organisation_id': self.organisation.id,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'urban'
                },
                {
                    'id': self.holding_1.id,
                    'layer': 'holding',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                },
            ]
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        # without adding to organisation, should return 400
        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        # add to organisation, should return 201
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation
        )
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)
        property = Property.objects.get(id=response.data['id'])
        self.assertEqual(property.name, data['name'])
        self.assertEqual(property.property_type.id, data['property_type_id'])
        self.assertEqual(property.province.id, data['province_id'])
        self.assertEqual(property.organisation.id, data['organisation_id'])
        self.assertEqual(
            Parcel.objects.filter(property=property).count(),
            2
        )
        # get property
        kwargs = {
            'id': property.id
        }
        request = self.factory.get(
            reverse('property-detail', kwargs=kwargs)
        )
        request.user = self.user_1
        view = PropertyDetail.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['bbox']), 4)
        self.assertEqual(len(response.data['parcels']), 2)

    def test_metadata_list(self):
        request = self.factory.get(
            reverse('property-metadata')
        )
        request.user = self.user_1
        view = PropertyMetadataList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_property_list(self):
        property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property C',
            created_by=self.user_2,
            organisation=self.organisation
        )
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        _property = response.data[0]
        self.assertEqual(_property['id'], property.id)
        self.assertEqual(_property['name'], property.name)

    def test_update_property(self):
        property_type = PropertyType.objects.all().first()
        property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property D',
            created_by=self.user_1
        )
        data = {
            'id': property.id,
            'name': 'Property D-1',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'province_id': self.province.id,
            'organisation_id': self.organisation.id,
            'parcels': []
        }
        request = self.factory.post(
            reverse('property-update-detail'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = UpdatePropertyInformation.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        updated = Property.objects.get(id=property.id)
        self.assertEqual(updated.name, data['name'])

    def test_update_boundaries(self):
        property_type = PropertyType.objects.all().first()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'province_id': self.province.id,
            'organisation_id': self.organisation.id,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'urban'
                },
                {
                    'id': self.holding_1.id,
                    'layer': 'holding',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                },
            ]
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        request.user = self.user_1
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation
        )
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        property_id = response.data['id']
        data = {
            'id': property_id,
            'parcels': [
                {
                    'id': self.holding_1.id,
                    'layer': 'holding',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                }
            ]
        }
        request = self.factory.post(
            reverse('property-update-boundaries'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = UpdatePropertyBoundaries.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Parcel.objects.filter(property_id=property_id).count(),
            1
        )
