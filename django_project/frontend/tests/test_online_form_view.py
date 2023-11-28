from frontend.tests.base_view import RegisteredBaseViewTestBase
from django.core.exceptions import PermissionDenied
from frontend.views.online_form import OnlineFormView
from django.urls import reverse
from property.factories import PropertyFactory
from population_data.factories import AnnualPopulationF
from frontend.tests.model_factories import UserF
from stakeholder.factories import organisationRepresentativeFactory, organisationUserFactory


class TestOnlineFormViewView(RegisteredBaseViewTestBase):
    view_name = 'online-form'
    view_cls = OnlineFormView

    def setUp(self) -> None:
        super().setUp()
        self.property = PropertyFactory.create(
            organisation=self.organisation_1
        )

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
