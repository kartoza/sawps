from django.contrib.auth.models import User
from django.test import TestCase

from frontend.static_mapping import REGIONAL_DATA_CONSUMER
from frontend.utils.user_roles import get_user_roles
from sawps.tests.models.account_factory import GroupF


class TestUserRoles(TestCase):

    def test_get_user_roles(self):
        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd',
            is_superuser=True
        )
        group = GroupF.create(name=REGIONAL_DATA_CONSUMER)
        user.groups.add(group)

        user_roles = get_user_roles(user)
        self.assertTrue('Super user' in user_roles)
        self.assertTrue(REGIONAL_DATA_CONSUMER in user_roles)

