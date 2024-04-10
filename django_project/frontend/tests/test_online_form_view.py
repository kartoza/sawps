from frontend.tests.base_view import RegisteredBaseViewTestBase
from django.core.exceptions import PermissionDenied
from frontend.views.online_form import OnlineFormView
from django.urls import reverse
from property.factories import PropertyFactory
from population_data.factories import AnnualPopulationF
from frontend.tests.model_factories import UserF
from sawps.tests.models.account_factory import GroupF
from stakeholder.factories import organisationRepresentativeFactory, organisationUserFactory
from frontend.static_mapping import (
    NATIONAL_DATA_CONSUMER,
    NATIONAL_DATA_SCIENTIST
)


class TestOnlineFormViewView(RegisteredBaseViewTestBase):
    view_name = 'online-form'
    view_cls = OnlineFormView

    def setUp(self) -> None:
        super().setUp()
        self.property = PropertyFactory.create(
            organisation=self.organisation_1
        )
        # add data consumer group
        self.data_consumer_group = GroupF.create(name=NATIONAL_DATA_CONSUMER)
        self.data_scientist_group = GroupF.create(name=NATIONAL_DATA_SCIENTIST)

    def test_online_form_view(self):
        kwargs = {
            'property_id': self.property.id
        }
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs))
        request.user = self.superuser
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        self.assertIn('upload_id', context)
        self.assertEqual(context['upload_id'], 0)

    def test_online_form_without_organisation(self):
        kwargs = {
            'property_id': self.property.id
        }
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs))
        request.user = self.user_2
        view = self.view_cls()
        view.setup(request)
        with self.assertRaises(PermissionDenied):
            context = view.get_context_data(**kwargs)
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs))
        request.user = self.user_1
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        # add user_1 to data consumer group
        self.user_1.groups.add(self.data_consumer_group)
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs))
        request.user = self.user_1
        view = self.view_cls()
        view.setup(request)
        with self.assertRaises(PermissionDenied):
            context = view.get_context_data(**kwargs)

    def test_with_upload_id(self):
        population = AnnualPopulationF.create(
            property=self.property,
            user=self.user_2
        )
        kwargs = {
            'property_id': self.property.id
        }
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = self.superuser
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        self.assertIn('upload_id', context)
        self.assertEqual(context['upload_id'], population.id)
        # test with any user
        user_3 = UserF.create()
        user_3.groups.add(self.group_member)
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = user_3
        view = self.view_cls()
        view.setup(request)
        with self.assertRaises(PermissionDenied):
            context = view.get_context_data(**kwargs)
        # test with manager
        organisationRepresentativeFactory.create(
            organisation=self.property.organisation,
            user=user_3
        )
        organisationUserFactory.create(
            organisation=self.property.organisation,
            user=user_3
        )
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = user_3
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        self.assertIn('upload_id', context)
        self.assertEqual(context['upload_id'], population.id)
        # test with data owner
        organisationUserFactory.create(
            organisation=self.property.organisation,
            user=self.user_2
        )
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = self.user_2
        view = self.view_cls()
        view.setup(request)
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        self.assertIn('upload_id', context)
        self.assertEqual(context['upload_id'], population.id)

    def test_upload_with_data_scientist(self):
        # add user_3 to data scientist group
        user_3 = UserF.create()
        user_3.groups.add(self.group_member)
        user_3.groups.add(self.data_scientist_group)
        population = AnnualPopulationF.create(
            property=self.property,
            user=user_3
        )
        kwargs = {
            'property_id': self.property.id
        }
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = user_3
        view = self.view_cls()
        view.setup(request)
        # data scientist can edit/upload data
        context = view.get_context_data(**kwargs)
        self.assertIn('property_id', context)
        self.assertEqual(context['property_id'], self.property.id)
        self.assertIn('upload_id', context)
        self.assertEqual(context['upload_id'], population.id)

    def test_edit_with_data_consumer(self):
        # add user_3 to data consumer group
        user_3 = UserF.create()
        user_3.groups.add(self.group_member)
        user_3.groups.add(self.data_consumer_group)
        population = AnnualPopulationF.create(
            property=self.property,
            user=user_3
        )
        kwargs = {
            'property_id': self.property.id
        }
        request = self.factory.get(reverse(self.view_name, kwargs=kwargs) + f'?upload_id={population.id}')
        request.user = user_3
        view = self.view_cls()
        view.setup(request)
        # data consumer cannnot edit/upload data
        with self.assertRaises(PermissionDenied):
            context = view.get_context_data(**kwargs)
