import base64
import json

import mock
import datetime
import uuid
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.settings.utils import absolute_path
from frontend.api_views.property import (
    CreateNewProperty,
    PropertyList,
    PropertyMetadataList,
    UpdatePropertyBoundaries,
    PropertyDetail,
    PropertySearch,
    UpdatePropertyInformation,
    CheckPropertyNameIsAvailable,
    ListPropertyTypeAPIView,
    ListProvince
)
from frontend.models.parcels import Erf, Holding
from frontend.models.places import (
    PlaceNameSmallScale,
    PlaceNameMidScale,
    PlaceNameLargerScale,
    PlaceNameLargestScale
)
from frontend.models.boundary_search import BoundarySearchRequest
from frontend.tests.model_factories import UserF
from frontend.tests.request_factories import OrganisationAPIRequestFactory
from population_data.models import OpenCloseSystem
from property.factories import PropertyFactory, ProvinceFactory, PropertyTypeFactory
from property.models import (
    Parcel, Property, PropertyType,
    BOUNDARY_FILE_SOURCE_TYPE, SELECT_SOURCE_TYPE,
    DIGITISE_SOURCE_TYPE
)
from stakeholder.factories import (
    organisationFactory,
    organisationUserFactory,
)
from frontend.static_mapping import (
    PROVINCIAL_DATA_SCIENTIST
)
from sawps.models import ExtendedGroup
from sawps.tests.model_factories import GroupF
from frontend.models.map_session import MapSession
from frontend.tests.test_map import is_materialized_view_exists
from frontend.utils.map import generate_map_view


class TestPropertyAPIViews(TestCase):
    fixtures = [
        'open_close_systems.json',
        'property_type.json',
        'parcel_types.json'
    ]

    def setUp(self) -> None:
        # insert organisation
        self.organisation = organisationFactory.create()
        self.factory = OrganisationAPIRequestFactory(self.organisation)
        self.user_1 = UserF.create(username='test_1')
        self.user_2 = UserF.create(username='test_2')
        # add group and permission
        self.group_1 = GroupF.create()
        content_type = ContentType.objects.get_for_model(ExtendedGroup)
        view_properties_perm = Permission.objects.filter(
            content_type=content_type,
            codename='can_view_map_properties_layer'
        ).first()
        self.group_1.permissions.add(view_properties_perm)
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

    @mock.patch('frontend.api_views.property.find_province')
    def test_create_new_property(self, mocked_find_province):
        mocked_find_province.return_value = self.province
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
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
                {
                    'id': self.holding_1.id,
                    'layer': 'farm_portion',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                },
                {
                    'id': 1001,
                    'layer': 'farm_portion',
                    'cname': 'C1001',
                    'type': 'urban'
                },
                {
                    'id': 1002,
                    'layer': 'parent_farm',
                    'cname': 'C1002',
                    'type': 'urban'
                },
            ]
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        # without adding to organisation, should return 403
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()

        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
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
        self.assertEqual(property.province.id, self.province.id)
        self.assertEqual(property.organisation.id, data['organisation_id'])
        self.assertEqual(property.open.id, data['open_id'])
        self.assertEqual(
            Parcel.objects.filter(property=property).count(),
            2
        )
        self.assertEqual(property.short_code, response.data['short_code'])
        self.assertEqual(property.boundary_source, SELECT_SOURCE_TYPE)
        self.assertEqual(response.data['boundary_source'], property.boundary_source)
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
        find_parcel = [p for p in response.data['parcels'] if p['id'] == self.erf_1.id and p['layer'] == 'erf']
        self.assertEqual(len(find_parcel), 1)
        self.assertEqual(response.data['short_code'], property.short_code)
        self.assertEqual(response.data['boundary_source'], property.boundary_source)
        # test insert with existing name should return 400
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('existing property with name Property A', response.data)

    @mock.patch('frontend.api_views.property.find_province')
    def test_create_new_property_parcel_not_exist(self, mocked_find_province):
        mocked_find_province.return_value = self.province
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'non-existing-type'
                }
            ]
        }
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
        self.assertEqual(response.status_code, 400)
        self.assertEquals(
            response.data,
            'Invalid parcel_type: non-existing-type'
        )

    @mock.patch('frontend.api_views.property.find_province')
    def test_create_new_property_province_not_exist(self, mocked_find_province):
        mocked_find_province.return_value = None
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'non-existing-type'
                }
            ]
        }
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
        self.assertEqual(response.status_code, 400)
        self.assertEquals(
            response.data,
            'Invalid Province! Please contact administrator to populate province table!'
        )

    @mock.patch('frontend.api_views.property.get_current_organisation_id')
    def test_create_new_property_organisation_not_exist(self, mocked_org_id):
        mocked_org_id.return_value = None
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [
                {
                    'id': self.erf_1.id,
                    'layer': 'erf',
                    'cname': self.erf_1.cname,
                    'type': 'non-existing-type'
                }
            ]
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )

        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEquals(response.data, 'Invalid Organisation!')

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
        self.user_2.user_profile.current_organisation = self.organisation
        self.user_2.save()

        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        _property = response.data[0]
        self.assertEqual(_property['id'], property.id)
        self.assertEqual(_property['name'], property.name)
        self.assertEqual(_property['short_code'], property.short_code)
        # test provincial data scientist
        provincial_ds_group, _ = Group.objects.get_or_create(name=PROVINCIAL_DATA_SCIENTIST)
        self.user_2.groups.add(provincial_ds_group)
        organisation_2 = organisationFactory.create(
            national=False,
            province=self.province
        )
        property_2 = PropertyFactory.create(
            province=self.province,
            organisation=organisation_2
        )
        # test with empty current organisation
        self.user_2.user_profile.current_organisation = None
        self.user_2.save()
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # test with empty province
        self.user_2.user_profile.current_organisation = organisation_2
        self.user_2.save()
        organisation_2.province = None
        organisation_2.save()
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        # test if provincial role then can see property in same province
        organisation_2.province = self.province
        organisation_2.save()
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        find_property = [prop for prop in response.data if prop['id'] == property_2.id]
        self.assertEqual(len(find_property), 1)
        # test if provincial role then cannot see property in other province
        property_3 = PropertyFactory.create(
            organisation=organisation_2
        )
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        find_property = [prop for prop in response.data if prop['id'] == property_3.id]
        self.assertEqual(len(find_property), 0)
        # test if other roles, then can only see from organisation parameters
        self.user_2.groups.remove(provincial_ds_group)
        request = self.factory.get(
            reverse('property-list')
        )
        request.user = self.user_2
        view = PropertyList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        find_property = [prop for prop in response.data if prop['id'] == property_3.id]
        self.assertEqual(len(find_property), 1)

    def test_get_property_list_for_organisations(self):
        """Taxon list API test for organisations."""
        organisation = organisationFactory.create(national=True)

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )

        user.user_profile.current_organisation = organisation
        user.save()

        property = PropertyFactory.create(
            organisation=organisation,
            name='PropertyA'
        )

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }

        url = reverse("property-list")
        client = Client()
        data = {"organisation":organisation.id}
        response = client.get(url, data, **auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "PropertyA")

    def test_property_list_with_organisation_id(self):
        organisation = organisationFactory.create(national=True)

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )

        user.user_profile.current_organisation = organisation
        user.save()
        # Create properties related to the organisation
        property1 = PropertyFactory.create(
            organisation=organisation,
            name='PropertyA'
        )
        property2 = PropertyFactory.create(
            organisation=organisation,
            name='PropertyB'
        )

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }

        url = reverse("property-list", kwargs={'organisation_id': organisation.id})
        client = Client()
        response = client.get(url, **auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "PropertyA")
        self.assertEqual(response.data[1]['name'], "PropertyB")

    def test_property_list_multiple_organisations_data_contributor(self):
        """
        Test property list for data contributor, which will only return
        property directly related to their current organisation.
        """
        organisation = organisationFactory.create(national=True)
        organisation_2 = organisationFactory.create(national=False)

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )

        organisationUserFactory.create(
            user=user,
            organisation=organisation
        )

        user.user_profile.current_organisation = organisation
        user.save()
        # Create properties related to the organisation
        PropertyFactory.create(
            organisation=organisation,
            name='PropertyA'
        )
        PropertyFactory.create(
            organisation=organisation,
            name='PropertyB'
        )
        PropertyFactory.create(
            organisation=organisation_2,
            name='PropertyC'
        )

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }

        url = reverse("property-list")
        client = Client()
        response = client.get(
            url,
            {'organisation': f'{organisation.id}, {organisation_2.id}'},
            **auth_headers
        )

        # PropertyC is not returned because it does not belong to
        # user's current organisation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], "PropertyA")
        self.assertEqual(response.data[1]['name'], "PropertyB")
        self.assertEqual(response.data[2]['name'], "PropertyC")

    def test_property_list_multiple_organisations_data_scientist(self):
        """
        Test property list for data scientist, which will return
        all property related to the organisation ID supplied in parameter.
        """
        organisation = organisationFactory.create(national=True)
        organisation_2 = organisationFactory.create(national=False)

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )

        user.user_profile.current_organisation = organisation
        user.save()
        # Create properties related to the organisation
        PropertyFactory.create(
            organisation=organisation,
            name='PropertyA'
        )
        PropertyFactory.create(
            organisation=organisation,
            name='PropertyB'
        )
        PropertyFactory.create(
            organisation=organisation_2,
            name='PropertyC'
        )

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }

        url = reverse("property-list")
        client = Client()
        response = client.get(
            url,
            {'organisation': f'{organisation.id}, {organisation_2.id}'},
            **auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], "PropertyA")
        self.assertEqual(response.data[1]['name'], "PropertyB")
        self.assertEqual(response.data[2]['name'], "PropertyC")

    def test_property_list_without_organisation_id(self):
        organisation = organisationFactory.create(national=True)

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )

        user.user_profile.current_organisation = organisation
        user.save()

        # Create properties related to the organisation
        property1 = PropertyFactory.create(
            organisation=organisation,
            name='PropertyA'
        )
        property2 = PropertyFactory.create(
            organisation=organisation,
            name='PropertyB'
        )
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }

        url = reverse("property-list")
        client = Client()
        response = client.get(url, **auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "PropertyA")
        self.assertEqual(response.data[1]['name'], "PropertyB")

    @mock.patch('frontend.api_views.property.find_province')
    def test_update_property(self, mocked_find_province):
        mocked_find_province.return_value = self.province
        property_type = PropertyType.objects.all().first()
        property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property D',
            created_by=self.user_1
        )
        open_close_system = OpenCloseSystem.objects.first()
        data = {
            'id': property.id,
            'name': 'Property D-1',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
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
        self.assertEqual(updated.open_id, data['open_id'])
        # add other property and assert cannot use same name
        other_property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property ABCD',
            created_by=self.user_1
        )
        data['name'] = other_property.name
        request = self.factory.post(
            reverse('property-update-detail'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = UpdatePropertyInformation.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('existing property with name Property ABCD',
                      response.data)

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
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()

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
        updated = Property.objects.get(id=property_id)
        self.assertEqual(response.data['short_code'], updated.short_code)

    def test_search_property(self):
        # insert place names
        place_1 = PlaceNameSmallScale.objects.create(
            geom=self.holding_1.geom.centroid,
            fclass='suburb',
            name='Seaview'
        )
        place_2 = PlaceNameMidScale.objects.create(
            geom=self.holding_1.geom.centroid,
            fclass='suburb',
            name='Seaview'
        )
        place_3 = PlaceNameLargerScale.objects.create(
            geom=self.holding_1.geom.centroid,
            fclass='hamlet',
            name='Sea Glade'
        )
        place_4 = PlaceNameLargestScale.objects.create(
            geom=self.holding_1.geom.centroid,
            fclass='town',
            name='SeaCow Lake'
        )
        # insert property
        property = PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Seafields',
            created_by=self.user_2,
            organisation=self.organisation
        )
        request = self.factory.get(
            reverse('property-search') + '?search_text=sea'
        )
        self.user_2.user_profile = self.user_2.user_profile
        self.user_2.user_profile.current_organisation = self.organisation
        self.user_2.save()

        request.user = self.user_2
        view = PropertySearch.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        # add to the group
        self.user_2.groups.add(self.group_1)
        request.user = self.user_2
        view = PropertySearch.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        # search by short_code
        request = self.factory.get(
            reverse('property-search') + f'?search_text={property.short_code}'
        )
        request.user = self.user_2
        view = PropertySearch.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'],
                         f'{property.name} ({property.short_code})')
        # test using map session
        filter_organisation = 'all'
        filter_spatial = ''
        filter_property = 'all'
        filter_year = 2023
        filter_species_name = ''
        filter_activity = ''
        session = MapSession.objects.create(
            user=self.user_1,
            created_date=datetime.datetime(2000, 8, 14, 8, 8, 8),
            expired_date=datetime.datetime(2000, 8, 14, 8, 8, 8),
            species=filter_species_name
        )
        # generate materialized view for properties layer
        generate_map_view(session, False, filter_year,
                          filter_species_name, filter_organisation,
                          filter_activity, filter_spatial, filter_property)
        self.assertTrue(
            is_materialized_view_exists(session.properties_view_name))
        request = self.factory.get(
            reverse('property-search') + f'?search_text=sea&session={str(session.uuid)}'
        )
        request.user = self.user_2
        view = PropertySearch.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_check_property_name(self):
        data = {
            'name': 'Property ABC'
        }
        request = self.factory.post(
            reverse('property-check-available-name'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CheckPropertyNameIsAvailable.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['available'])
        PropertyFactory.create(
            geometry=self.holding_1.geom,
            name='Property ABC',
            created_by=self.user_1
        )
        request = self.factory.post(
            reverse('property-check-available-name'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CheckPropertyNameIsAvailable.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['available'])

    def test_create_new_property_from_boundary_upload(self):
        search_request = BoundarySearchRequest.objects.create(
            type='File',
            session=str(uuid.uuid4()),
            request_by=self.user_1,
            geometry=self.erf_1.geom.transform(4326, clone=True),
            province=self.province,
            property_size_ha=10
        )
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        
        # add to organisation, should return 201
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation
        )
        # invalid search session
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [],
            'boundary_search_session': str(uuid.uuid4())
        }
        request = self.factory.post(
            reverse('property-create'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = CreateNewProperty.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        # should success
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [],
            'boundary_search_session': search_request.session
        }
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
        self.assertEqual(property.province.id, self.province.id)
        self.assertEqual(property.organisation.id, data['organisation_id'])
        self.assertEqual(property.open.id, data['open_id'])
        self.assertEqual(property.property_size_ha, search_request.property_size_ha)
        self.assertEqual(
            Parcel.objects.filter(property=property).count(),
            0
        )
        self.assertEqual(property.short_code, response.data['short_code'])
        self.assertEqual(property.boundary_source, BOUNDARY_FILE_SOURCE_TYPE)
        # test update with ranndom session
        data = {
            'id': property.id,
            'parcels': [],
            'boundary_search_session': str(uuid.uuid4())
        }
        request = self.factory.post(
            reverse('property-update-boundaries'), data=data,
            format='json'
        )
        request.user = self.user_1
        view = UpdatePropertyBoundaries.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        # test update should success
        search_request_2 = BoundarySearchRequest.objects.create(
            type='File',
            session=str(uuid.uuid4()),
            request_by=self.user_1,
            geometry=self.holding_1.geom.transform(4326, clone=True),
            province=self.province,
            property_size_ha=10
        )
        data = {
            'id': property.id,
            'parcels': [],
            'boundary_search_session': search_request_2.session
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
            Parcel.objects.filter(property_id=property.id).count(),
            0
        )

    def test_create_new_property_from_digitise(self):
        search_request = BoundarySearchRequest.objects.create(
            type='Digitise',
            session=str(uuid.uuid4()),
            request_by=self.user_1,
            geometry=self.erf_1.geom.transform(4326, clone=True),
            province=self.province,
            property_size_ha=10
        )
        property_type = PropertyType.objects.all().first()
        open_close_system = OpenCloseSystem.objects.all().first()
        
        # add to organisation, should return 201
        self.user_1.user_profile = self.user_1.user_profile
        self.user_1.user_profile.current_organisation = self.organisation
        self.user_1.save()
        organisationUserFactory.create(
            user=self.user_1,
            organisation=self.organisation
        )
        data = {
            'name': 'Property A',
            'owner_email': 'test@test.com',
            'property_type_id': property_type.id,
            'organisation_id': self.organisation.id,
            'open_id': open_close_system.id,
            'parcels': [
                {
                    'id': self.holding_1.id,
                    'layer': 'holding',
                    'cname': self.holding_1.cname,
                    'type': 'urban'
                }
            ],
            'boundary_search_session': search_request.session
        }
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
        self.assertEqual(property.province.id, self.province.id)
        self.assertEqual(property.organisation.id, data['organisation_id'])
        self.assertEqual(property.open.id, data['open_id'])
        self.assertTrue(property.property_size_ha > 0)
        self.assertEqual(
            Parcel.objects.filter(property=property).count(),
            1
        )
        self.assertEqual(property.short_code, response.data['short_code'])
        self.assertEqual(property.boundary_source, DIGITISE_SOURCE_TYPE)


class TestPropertyTypeList(TestCase):
    def test_check_property_name(self):
        user_1 = UserF.create(username='test_1')
        prop_type_1 = PropertyTypeFactory.create()
        prop_type_2 = PropertyTypeFactory.create()
        request = APIRequestFactory().get(
            reverse('property-types'),
            format='json'
        )
        request.user = user_1
        view = ListPropertyTypeAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            [
                {
                    'id': prop_type_1.id,
                    'name': prop_type_1.name,
                    'colour': prop_type_1.colour,
                },
                {
                    'id': prop_type_2.id,
                    'name': prop_type_2.name,
                    'colour': prop_type_2.colour,
                }
            ]
        )


class TestProvinceList(TestCase):
    def test_province_list(self):
        user_1 = UserF.create(username='test_1')
        province_1 = ProvinceFactory.create()
        province_2 = ProvinceFactory.create()
        request = APIRequestFactory().get(
            reverse('province-list'),
            format='json'
        )
        request.user = user_1
        view = ListProvince.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            [
                {
                    'id': province_1.id,
                    'name': province_1.name
                },
                {
                    'id': province_2.id,
                    'name': province_2.name
                }
            ]
        )
