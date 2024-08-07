import mock
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.test import TestCase, override_settings
from django.db.models.signals import post_save

from property.models import Province
from property.factories import PropertyFactory
from regulatory_permit.models import DataUsePermission
from stakeholder.factories import (
    loginStatusFactory,
    organisationFactory,
    organisationRepresentativeFactory,
    organisationUserFactory,
    userLoginFactory,
    userRoleTypeFactory,
    userTitleFactory,
)
from stakeholder.models import (
    LoginStatus,
    Organisation,
    OrganisationInvites,
    OrganisationRepresentative,
    OrganisationUser,
    Reminders,
    UserLogin,
    UserProfile,
    UserRoleType,
    UserTitle,
    create_user_profile,
    save_user_profile,
    MANAGER,
    MEMBER
)
from sawps.tests.model_factories import GroupF
from frontend.static_mapping import (
    ORGANISATION_MANAGER,
    ORGANISATION_MEMBER
)
from species.factories import UserFactory


def mocked_sending_email(*args, **kwargs):
    return True


class TestUserRoleType(TestCase):
    """Test user's role type model."""

    @classmethod
    def setUpTestData(cls):
        cls.UserRoleTypeFactory = userRoleTypeFactory()

    def test_create_new_role(self):
        """Test creating new role."""
        self.assertEqual(UserRoleType.objects.count(), 1)
        self.assertTrue(
            self.UserRoleTypeFactory.name
            in ['base user', 'admin', 'super user']
        )

    def test_update_role(self):
        """Test updating a role."""
        self.UserRoleTypeFactory.name = 'admin'
        self.UserRoleTypeFactory.save()
        UserRoleObject = UserRoleType.objects.get(
            id=self.UserRoleTypeFactory.id
        )
        self.assertEqual(UserRoleObject.name, 'admin')

    def test_delete_role(self):
        """Test deleting new role."""
        self.UserRoleTypeFactory.delete()
        self.assertEqual(UserRoleType.objects.count(), 0)


class UserTitleTestCase(TestCase):
    """User title test case."""

    @classmethod
    def setUpTestData(cls):
        cls.userTitle = userTitleFactory()

    def test_create_new_title(self):
        """Test creating new title."""
        self.assertEqual(UserTitle.objects.count(), 1)
        self.assertTrue(self.userTitle.name in ['mr', 'mrs', 'miss', 'dr'])

    def test_update_title(self):
        """Test updating a title."""
        self.userTitle.name = 'mr'
        userTitle = UserTitle.objects.get(id=self.userTitle.id)
        self.assertTrue(userTitle.name, 'mr')

    def test_delete_new_title(self):
        """Test deleting a title."""
        self.userTitle.delete()
        self.assertEqual(UserTitle.objects.count(), 0)


class LoginStatusTestCase(TestCase):
    """User login status test case."""

    @classmethod
    def setUpTestData(cls):
        cls.loginStatus = loginStatusFactory()

    def test_create_login_status(self):
        """Test creating login status."""
        self.assertEqual(LoginStatus.objects.count(), 1)
        self.assertTrue(
            isinstance(self.loginStatus, LoginStatus)
        )
        self.assertTrue(self.loginStatus.name in ['logged in', 'logged out'])

    def test_update_login_status(self):
        """Test updating a login status."""
        self.loginStatus.name = 'logged in'
        loginStatus = LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged in')
        self.loginStatus.name = 'logged out'
        loginStatus = LoginStatus.objects.get(
            id=self.loginStatus.id
        )
        self.assertTrue(loginStatus.name, 'logged out')

    def test_delete_login_status(self):
        """Test deleting a login status."""
        self.loginStatus.delete()
        self.assertEqual(LoginStatus.objects.count(), 0)


class TestUser(TestCase):
    """Test the main user model relation to the profie model."""

    @classmethod
    def setUpTestData(cls):
        cls.user_profile = User.objects.create().user_profile

    def test_create_new_user_with_new_profile(self):
        """Test creating new user when new profile is created."""
        self.assertGreater(UserProfile.objects.count(), 0)

    def test_update_user_profile(self):
        """Test updating user through profile."""
        self.user_profile.user.username = 'test'
        self.user_profile.user.first_name = 'test123'
        self.user_profile.user.save()
        self.assertEqual(
            User.objects.get(username='test').first_name, 'test123'
        )

    def test_delete_profile(self):
        """Test deleting user when a profile is deleted."""
        user_id = self.user_profile.user.id
        self.user_profile.delete()
        self.assertEqual(User.objects.count(), 1)

        users = User.objects.filter(id=user_id)
        self.assertFalse(users.exists())

    def test_create_user_without_profile(self):
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        user = User.objects.create(username='test999')
        self.assertFalse(UserProfile.objects.filter(
            user_id=user.id
        ).exists())
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)

        user.save()
        self.assertTrue(UserProfile.objects.filter(
            user_id=user.id
        ).exists())

    def test_user_not_exist(self):
        self.assertEqual(
            self.user_profile.__str__(),
            self.user_profile.user.username
        )
        self.user_profile.user_id = 99999999999
        self.assertEqual(
            self.user_profile.__str__(),
            str(self.user_profile.id)
        )


class TestUserLogin(TestCase):
    """"User login testcase."""

    @classmethod
    def setUpTestData(cls):
        cls.user_login = userLoginFactory()

    def create_user_login(self):
        """Test creating new user login."""
        self.assertEqual(UserLogin.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user_login(self):
        """Test updating user login."""
        self.user_login.login_status.name = 'logged out'
        self.user_login.login_status.save()
        self.assertEqual(
            UserLogin.objects.get(id=self.user_login.id).login_status.name,
            'logged out'
        )

    def test_delete_user_login(self):
        """Test deleting user login."""
        self.user_login.delete()
        self.assertEqual(UserLogin.objects.count(), 0)
        self.assertEqual(User.objects.count(), 2)

    def test_user_not_exist(self):
        self.assertEqual(
            self.user_login.__str__(),
            self.user_login.user.username
        )
        self.user_login.user_id = 99999999999
        self.assertEqual(
            self.user_login.__str__(),
            str(self.user_login.id)
        )


@override_settings(
    CELERY_ALWAYS_EAGER=True,
    BROKER_BACKEND='memory',
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
)
class OrganizationTestCase(TestCase):
    """Organization test case."""

    @classmethod
    def setUpTestData(cls):
        cls.organization = organisationFactory(
            name='CapeNature'
        )

    def test_create_organization(self):
        """Test creating organization."""
        self.assertEqual(Organisation.objects.count(), 1)
        self.assertTrue(isinstance(self.organization, Organisation))
        self.assertTrue(self.organization.name, Organisation.objects.get(
            id=self.organization.id).name)
        self.assertEqual(
            self.organization.short_code,
            'CA0001'
        )

    def test_update_organization(self):
        """Test updating organization."""
        province, created = Province.objects.get_or_create(
                    name="Limpopo"
        )
        property_1 = PropertyFactory.create(
            organisation=self.organization,
            province=province
        )
        property_2 = PropertyFactory.create(
            organisation=self.organization,
            province=province
        )
        self.organization.name = 'test'
        self.organization.national = True
        self.organization.province = province
        self.organization.save()
        self.organization.refresh_from_db()
        property_1.refresh_from_db()
        property_2.refresh_from_db()
        self.assertEqual(Organisation.objects.get(
            id=self.organization.id).name, 'test')
        self.assertEqual(Organisation.objects.filter(
            national=True).count(), 1)
        self.assertEqual(Organisation.objects.filter(
            province__name="Limpopo").count(), 1)

        self.assertEqual(
            self.organization.short_code,
            'LITE0001'
        )

    def test_delete_organization(self):
        """Test deleting organization."""
        self.organization.delete()
        self.assertEqual(Organisation.objects.count(), 0)


class OrganizationUserTestCase(TestCase):
    """Test case for organization user."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    @classmethod
    def setUpTestData(cls):
        """Setup test data for organisation user model."""
        cls.organizationUser = organisationUserFactory()
        cls.user = UserFactory()
        cls.organisation = organisationFactory()

    def test_create_organisation_user_default(self):
        """Test creating organisation user, defaulted to Organisation Member."""
        self.assertEqual(OrganisationUser.objects.count(), 1)
        self.assertTrue(isinstance(self.organizationUser, OrganisationUser))
        self.assertEqual(
            self.organizationUser.user.groups.first().name,
            ORGANISATION_MEMBER
        )

    def test_create_organisation_user_manager(self):
        """Test creating organisation user as manager."""
        OrganisationRepresentative.objects.create(
            user=self.user,
            organisation=self.organisation
        )
        groups = Group.objects.filter(
            user=self.user
        )
        all_groups = [group.name for group in groups]
        self.assertIn(
            ORGANISATION_MANAGER,
            all_groups
        )
        self.assertIn(
            ORGANISATION_MEMBER,
            all_groups
        )

    def test_create_organisation_user_member(self):
        """Test creating organisation user as member."""
        OrganisationInvites.objects.create(
            email=self.user.email,
            joined=True,
            assigned_as=MEMBER,
            organisation=self.organisation
        )
        organisation_user = organisationUserFactory(
            user=self.user,
            organisation=self.organisation
        )
        self.assertEqual(
            organisation_user.user.groups.first().name,
            ORGANISATION_MEMBER
        )

    def test_update_organisation_user(self):
        """ Test updating organisation user."""
        self.organizationUser.user.username = 'test'
        self.organizationUser.user.save()
        self.assertEqual(
            self.organizationUser.user.username,
            'test'
        )

    def test_delete_organisation_user(self):
        """Test deleting organisation user."""
        user = self.organizationUser.user
        group = GroupF.create(name='Data contributor')
        user.groups.add(group)
        organisation_user_2 = organisationUserFactory.create(
            user=user
        )

        OrganisationInvites.objects.create(
            email=self.user.email,
            joined=True,
            assigned_as=MEMBER,
            organisation=self.organisation
        )
        organisation_user_3 = organisationUserFactory(
            user=self.user,
            organisation=self.organisation
        )
        organisation_user_4 = organisationUserFactory(
            user=self.user
        )
        self.assertEquals(
            list(organisation_user_3.user.groups.values_list('name', flat=True)),
            [ORGANISATION_MEMBER]
        )

        # delete organizationUser
        # user would still be in group Organisation Member
        # because he still belongs to other organisation
        self.organizationUser.delete()
        self.assertEqual(OrganisationUser.objects.count(), 3)
        self.assertEqual(len(user.groups.all()), 1)
        self.assertEqual(user.groups.first().name, ORGANISATION_MEMBER)

        # set userprofile to organisation 4
        user_profile = UserProfile.objects.filter(user=organisation_user_2.user).first()
        self.assertTrue(user_profile)
        user_profile.current_organisation = organisation_user_4.organisation
        user_profile.save()
        # delete organisation_user_2
        # user would be removed from group Organisation Member
        # because he no longer belongs any organisation
        organisation_user_2.delete()
        self.assertEqual(OrganisationUser.objects.count(), 2)
        self.assertFalse(
            user.groups.exists()
        )
        # ensure current_organisation is not removed
        user_profile.refresh_from_db()
        self.assertTrue(user_profile.current_organisation)
        self.assertEqual(user_profile.current_organisation.id, organisation_user_4.organisation.id)

        # set userprofile to organisation 4
        user_profile = UserProfile.objects.filter(user=organisation_user_4.user).first()
        self.assertTrue(user_profile)
        user_profile.current_organisation = organisation_user_4.organisation
        user_profile.save()
        # set as manager
        OrganisationRepresentative.objects.create(
            user=organisation_user_4.user,
            organisation=organisation_user_4.organisation
        )
        # create invite
        OrganisationInvites.objects.create(
            organisation=organisation_user_4.organisation,
            email=organisation_user_4.user.email,
            user=organisation_user_4.user,
        )
        # delete organisation_user_4
        # user would not be removed from group Organisation Member
        # because is still a member of other organisation
        organisation_user_4.delete()
        self.assertEqual(OrganisationUser.objects.count(), 1)
        self.assertEquals(
            list(self.user.groups.values_list('name', flat=True)),
            [ORGANISATION_MEMBER]
        )
        # ensure no current_organisation after organisation 4 is deleted
        user_profile.refresh_from_db()
        self.assertFalse(user_profile.current_organisation)
        # ensure no manager record
        self.assertFalse(OrganisationRepresentative.objects.filter(
            user=organisation_user_4.user,
            organisation=organisation_user_4.organisation
        ).exists())
        # ensure no invitation
        self.assertFalse(OrganisationInvites.objects.filter(
            user=organisation_user_4.user,
            organisation=organisation_user_4.organisation
        ).exists())


class OrganizationRepresentativeTestCase(TestCase):
    """Test case for organization representative."""

    @classmethod
    def setUpTestData(cls):
        """Setup test data for organisation representative model."""
        cls.organizationRep = organisationRepresentativeFactory()

    def test_create_organisation_user(self):
        """Test creating organisation representative."""
        self.assertEqual(OrganisationRepresentative.objects.count(), 1)
        self.assertTrue(
            isinstance(
                self.organizationRep,
                OrganisationRepresentative
            )
        )

    def test_update_organisation_user(self):
        """ Test updating organisation representative."""
        self.organizationRep.user.username = 'test'
        self.organizationRep.user.save()
        self.assertEqual(
            self.organizationRep.user.username,
            'test'
        )

    def test_delete_organisation_user(self):
        """Test deleting organisation representative."""
        self.organizationRep.delete()
        self.assertEqual(OrganisationRepresentative.objects.count(), 0)

    @mock.patch('stakeholder.utils.send_mail')
    def test_upgrade_to_manager(self, mocked_send_mail):
        """Test upgrade a member to manager."""
        mocked_send_mail.side_effect = mocked_sending_email
        organisation_1 = organisationFactory()
        # user without email
        user_0 = User.objects.create_user(
            username='testuser0',
            password='testpassword0'
        )
        OrganisationRepresentative.objects.create(
            user=user_0,
            organisation=organisation_1
        )
        mocked_send_mail.assert_not_called()
        self.assertTrue(OrganisationUser.objects.filter(
            user=user_0,
            organisation=organisation_1
        ).exists())
        # from no org_user - possible from admin site
        mocked_send_mail.reset_mock()
        user_1 = User.objects.create_user(
            username='testuser1',
            password='testpassword1',
            email='testuser1@test.com'
        )
        OrganisationRepresentative.objects.create(
            user=user_1,
            organisation=organisation_1
        )
        mocked_send_mail.assert_called_once()
        self.assertEqual(OrganisationUser.objects.filter(
            user=user_1,
            organisation=organisation_1
        ).count(), 1)
        # from existing org_user with invite = Member
        mocked_send_mail.reset_mock()
        user_2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            email='testuser2@test.com'
        )
        OrganisationUser.objects.create(
            user=user_2,
            organisation=organisation_1
        )
        OrganisationInvites.objects.create(
            user=user_2,
            joined=True,
            assigned_as=MEMBER
        )
        OrganisationRepresentative.objects.create(
            user=user_2,
            organisation=organisation_1
        )
        mocked_send_mail.assert_called_once()
        self.assertEqual(OrganisationUser.objects.filter(
            user=user_2,
            organisation=organisation_1
        ).count(), 1)
        # from existing org_user with invite = Manager
        mocked_send_mail.reset_mock()
        user_3 = User.objects.create_user(
            username='testuser3',
            password='testpassword3',
            email='testuser3@test.com'
        )
        OrganisationUser.objects.create(
            user=user_3,
            organisation=organisation_1
        )
        OrganisationInvites.objects.create(
            user=user_3,
            joined=True,
            assigned_as=MANAGER
        )
        OrganisationRepresentative.objects.create(
            user=user_3,
            organisation=organisation_1
        )
        mocked_send_mail.assert_not_called()
        self.assertEqual(OrganisationUser.objects.filter(
            user=user_3,
            organisation=organisation_1
        ).count(), 1)
        # from existing org_user without any invite
        mocked_send_mail.reset_mock()
        user_4 = User.objects.create_user(
            username='testuser4',
            password='testpassword4',
            email='testuser4@test.com'
        )
        OrganisationUser.objects.create(
            user=user_4,
            organisation=organisation_1
        )
        OrganisationRepresentative.objects.create(
            user=user_4,
            organisation=organisation_1
        )
        mocked_send_mail.assert_called_once()
        self.assertEqual(OrganisationUser.objects.filter(
            user=user_4,
            organisation=organisation_1
        ).count(), 1)


class OrganisationInvitesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.organisation = Organisation.objects.create(
            name="test_organisation"
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )

    def test_create_organisation_invite(self):
        """Test create organisation invite."""
        invite = OrganisationInvites.objects.create(
            organisation=self.organisation, email='test@kartoza.com')
        self.assertEqual(invite.organisation, self.organisation)
        self.assertEqual(invite.email, 'test@kartoza.com')

    def test_read_organisation_invite(self):
        """Test read organisation invite."""
        invite = OrganisationInvites.objects.create(
            organisation=self.organisation, email='test@kartoza.com')
        saved_invite = OrganisationInvites.objects.get(pk=invite.pk)
        self.assertEqual(saved_invite.organisation, self.organisation)
        self.assertEqual(saved_invite.email, 'test@kartoza.com')

    def test_update_organisation_invite(self):
        """Test update organisation invite."""
        invite = OrganisationInvites.objects.create(
            organisation=self.organisation, email='test@kartoza.com')
        invite.organisation = self.organisation
        invite.save()
        updated_invite = OrganisationInvites.objects.get(pk=invite.pk)
        self.assertEqual(updated_invite.organisation, self.organisation)

    def test_delete_organisation_invite(self):
        """Test delete organisation invite."""
        invite = OrganisationInvites.objects.create(
            organisation=self.organisation, email='test@kartoza.com')
        invite.delete()
        self.assertFalse(
            OrganisationInvites.objects.filter(pk=invite.pk).exists())


class RemindersModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation"
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.reminder = Reminders.objects.create(
            title='test',
            user=self.user,
            organisation=self.organisation,
            reminder='reminder'
        )

    def test_create_reminder(self):
        reminder = Reminders.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.assertEqual(reminder.organisation, self.organisation)
        self.assertEqual(reminder.user, self.user)

    def test_get_reminder(self):
        reminder = Reminders.objects.get(
            organisation=self.organisation,
            user=self.user
        )
        self.assertEqual(reminder.organisation, self.organisation)
        self.assertEqual(reminder.title, self.reminder.title)

    def test_update_reminder(self):
        reminder = Reminders.objects.get(
            organisation=self.organisation,
            user=self.user
        )
        reminder.title = 'new'
        reminder.save()
        self.assertEqual(reminder.title, 'new')

    def test_delete_reminder_or_notif(self):
        reminder = Reminders.objects.get(
            organisation=self.organisation,
            user=self.user
        )
        reminder.delete()
        self.assertEqual(
            Reminders.objects.filter(
                user=self.user,
                organisation=self.organisation
            ).exists(), False)

    def test_search_remider_or_notification(self):
        reminders = Reminders.objects.filter(
            Q(user=self.user),
            Q(organisation=self.organisation),
            Q(title__icontains='t') | Q(
                reminder__icontains='t')
        )

        self.assertEqual(len(reminders), 1)
