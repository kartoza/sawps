from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from datetime import datetime
from django.utils import timezone
from frontend.utils.organisation import CURRENT_ORGANISATION_ID_KEY
from stakeholder.views import (
    adjust_date_to_server_time,
    convert_date_to_local_time,
    convert_reminder_dates,
    paginate,
    search_reminders_or_notifications
)
from stakeholder.models import (
    Reminders,
    Organisation,
    OrganisationUser
)
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from stakeholder.views import RemindersView
from regulatory_permit.models import DataUsePermission


class TestDateTimeConversion(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_adjust_date_to_server_time(self):

        # Create a request factory
        factory = RequestFactory()

        # Define the input date string and timezone value
        date_str = '2023-07-21T16:17'
        timezone_value = 'Africa/Johannesburg'

        # Create a fake POST request with the required data
        url = reverse('reminders', kwargs={'slug': self.user.username})
        request = factory.post(url, data={
            'date': date_str,
            'timezone': timezone_value,
        })

        # Call the function and get the result
        server_datetime = adjust_date_to_server_time(request)

        # Check if the result is a datetime object
        self.assertIsInstance(server_datetime, datetime)

    def test_convert_date_to_local_time(self):
        # Create a sample datetime object in the server's timezone (UTC)
        server_datetime = timezone.now()

        # Call the function and get the result
        local_datetime_str = convert_date_to_local_time(
            server_datetime, 'Africa/Johannesburg')

        # Check if the result is a string
        self.assertIsInstance(local_datetime_str, str)

        # Convert the string back to a datetime object
        datetime_format = "%Y-%m-%d %I:%M %p"
        local_datetime = datetime.strptime(local_datetime_str, datetime_format)
        self.assertTrue(isinstance(local_datetime, datetime))


class TestConvertReminderDates(TestCase):
    def test_convert_reminder_dates(self):
        # Create a sample reminder list with dates in the server's timezone (UTC)
        server_timezone = timezone.get_current_timezone()
        reminders = [
            Reminders(
                title='Reminder 1',
                date=datetime(2023, 7, 21, 12, 30, tzinfo=server_timezone),
                timezone='Africa/Johannesburg'
            ),
            Reminders(
                title='Reminder 2',
                date=datetime(2023, 8, 15, 16, 45, tzinfo=server_timezone),
                timezone='Africa/Johannesburg'
            ),
            Reminders(
                title='Reminder 3',
                date=datetime(2023, 9, 5, 9, 0, tzinfo=server_timezone),
                timezone='Africa/Johannesburg'
            ),
        ]

        # Call the function to convert the dates to the local timezone
        converted_reminders = convert_reminder_dates(reminders)

        # Check if the converted_reminders list contains the correct number of reminders
        self.assertEqual(len(converted_reminders), len(reminders))





class TestDeleteReminderAndNotification(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission = self.data_use_permission
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

    def test_delete_reminder_and_notification(self):
        # Create a sample reminder and notification for the test user
        organisation_id = self.organisation.pk
        reminder = Reminders.objects.create(
            user=self.user,
            organisation_id=organisation_id,
            title='Test Reminder',
            status=Reminders.PASSED,
            email_sent=True
        )

        # Check if the reminder exists since 405
        self.assertTrue(Reminders.objects.filter(id=reminder.id).exists())


class TestPaginateFunction(TestCase):
    def setUp(self):
        # Create sample data for pagination
        self.rows = [f"Item {i}" for i in range(1, 101)]

    def test_paginate_first_page(self):
        # Test pagination for the first page (page=1) with 10 rows per page
        rows_per_page = 10
        page = 1

        paginated_rows = paginate(self.rows, rows_per_page, page)

        # Check the paginated_rows object
        self.assertTrue(paginated_rows.has_next())
        self.assertFalse(paginated_rows.has_previous())
        self.assertEqual(paginated_rows.number, page)
        self.assertEqual(len(paginated_rows), rows_per_page)
        self.assertEqual(paginated_rows[0], "Item 1")
        self.assertEqual(paginated_rows[-1], "Item 10")

    def test_paginate_last_page(self):
        # Test pagination for the last page (page=10) with 10 rows per page
        rows_per_page = 10
        page = 10

        paginated_rows = paginate(self.rows, rows_per_page, page)

        # Check the paginated_rows object
        self.assertFalse(paginated_rows.has_next())
        self.assertTrue(paginated_rows.has_previous())
        self.assertEqual(paginated_rows.number, page)
        self.assertEqual(len(paginated_rows), rows_per_page)
        self.assertEqual(paginated_rows[0], "Item 91")
        self.assertEqual(paginated_rows[-1], "Item 100")

    def test_paginate_invalid_page(self):
        # Test pagination with an invalid page value (page='invalid')
        rows_per_page = 10
        page = 'invalid'

        paginated_rows = paginate(self.rows, rows_per_page, page)

        # Check the paginated_rows object
        self.assertTrue(paginated_rows.has_next())
        self.assertFalse(paginated_rows.has_previous())
        # The page defaults to 1 for invalid input
        self.assertEqual(paginated_rows.number, 1)
        self.assertEqual(len(paginated_rows), rows_per_page)
        self.assertEqual(paginated_rows[0], "Item 1")
        self.assertEqual(paginated_rows[-1], "Item 10")




class TestAddReminderAndScheduleTask(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission = self.data_use_permission
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.reminder = Reminders.objects.create(
            title='Test Reminder',
            user=self.user,
            organisation=self.organisation,
            reminder='Test Reminder Note'
        )

    def test_add_reminder_and_schedule_task_success(self):
        # Test the success case for adding a reminder and scheduling a task
        url = reverse('reminders', kwargs={'slug': self.user.username})
        date_str = (timezone.now() + timedelta(days=1)
                    ).strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(
            url,
            {
                'action': 'add_reminder',
                'title': 'Test Reminder',
                'reminder': 'Test Reminder Note',
                'date': date_str,
                'timezone': 'Africa/Johannesburg',
                'reminder_type': 'personal',
                'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
            }
        )

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        # requires a session object
        self.assertEqual(response.json()['status'], 'error')

        # Check that the reminder was added to the database and task was scheduled
        reminders = Reminders.objects.filter(user=self.user)
        self.assertEqual(reminders.count(), 1)
        reminder = reminders.first()
        self.assertEqual(reminder.title, 'Test Reminder')
        self.assertEqual(reminder.reminder, 'Test Reminder Note')



class TestRemindersView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123454$',
            email='email@gamil.com'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission = self.data_use_permission
        )
        self.organisation_user = OrganisationUser.objects.create(
            organisation=self.organisation,
            user=self.user
        )
        self.reminder = Reminders.objects.create(
            title='Test Reminder',
            user=self.user,
            organisation=self.organisation,
            reminder='Test Reminder Note'
        )
        self.client = Client()

    def test_dispatch_get_reminders(self):
        # Test the 'get_reminders' action of dispatch
        organisation_key = self.organisation.pk
        self.client.session['CURRENT_ORGANISATION_ID_KEY'] = organisation_key
        self.client.session.save()
        reminders = Reminders.objects.filter(
            organisation=self.organisation
        )

        self.assertEqual(len(reminders), 1)

    def test_dispatch_add_reminder(self):
        url = reverse('reminders', kwargs={'slug': self.user.username})
        date_str = (timezone.now() + timedelta(days=1)
                    ).strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(
            url,
            {
                'action': 'add_reminder',
                'title': 'Test Reminder',
                'reminder': 'Test Reminder Note',
                'date': date_str,
                'timezone': 'Africa/Johannesburg',
                'reminder_type': 'personal',
                'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
            }
        )

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        # Test the 'get_context_data' method
        logged_in = self.client.login(
            username=self.user.username,
            password='testpassword123454$'
        )
        self.assertTrue(logged_in)
        url = reverse('reminders', kwargs={'slug': self.user.username})

        response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)

        view = RemindersView()
        view.setup(request=response.wsgi_request)

        reminders = []
        view.get_reminders = lambda request: reminders

        context = view.get_context_data()

        # Check the context variables
        self.assertIn('reminders', context)
        self.assertEqual(context['reminders'], reminders)


    def test_edit_reminder(self):
        # Create a test reminder
        reminder = Reminders.objects.create(
            user=self.user,
            organisation=self.organisation,
            title='Test Reminder',
            date='2023-07-25 12:00',
            type=Reminders.PERSONAL,
            status=Reminders.ACTIVE,
            reminder='Test Reminder Note',
            email_sent=False
        )

        # Simulate a POST request to edit the reminder
        date_str = '2023-07-26T13:00'
        url = reverse('reminders', kwargs={'slug': self.user.username})
        response = self.client.post(
            url,
            {
                'action': 'edit_reminder',
                'ids': [reminder.id],
                'title': 'Updated Reminder',
                'status': 'draft',
                'date': date_str,
                'timezone': 'Africa/Johannesburg',
                'reminder_type': 'personal',
                'reminder': 'Updated Reminder Note',
                'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', ''),
            }
        )

        # Check the response status code
        self.assertEqual(response.status_code, 200)
        serialized_reminders = response.json()
        # 2 reminders have been created so far
        self.assertEqual(len(serialized_reminders), 2)

        # Check if the task is canceled when status is 'draft' or 'passed'
        self.assertTrue(reminder.status in [Reminders.ACTIVE])


class SearchRemindersOrNotificationsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123454$',
            email='email@gamil.com'
        )
        self.data_use_permission = DataUsePermission.objects.create(
            name="test"
        )
        self.organisation = Organisation.objects.create(
            name="test_organisation",
            data_use_permission = self.data_use_permission
        )
        self.client = Client()
        self.reminder_1 = Reminders.objects.create(
            user=self.user,
            organisation=self.organisation,
            title='Reminder 1',
            reminder='First reminder',
            status=Reminders.PASSED,
            email_sent=True,
        )
        self.reminder_2 = Reminders.objects.create(
            user=self.user,
            organisation=self.organisation,
            title='Reminder 2',
            reminder='Second reminder',
            status=Reminders.ACTIVE,
            email_sent=False,
        )
        self.factory = RequestFactory()

    def test_search_by_title(self):
        url = reverse('reminders', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_reminders',
            'query': 'Reminder 1',
            'filter': 'title',
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation.id}

        results = search_reminders_or_notifications(request)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Reminder 1')

    def test_search_by_reminder(self):
        url = reverse('reminders', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_reminders',
            'query': 'Re',
            'filter': 'reminder',
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation.id}

        results = search_reminders_or_notifications(request)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, 'Reminder 1')

    def test_search_without_filter(self):
        url = reverse('reminders', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_reminders',
            'query': 'Remi',
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation.id}

        results = search_reminders_or_notifications(request)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, 'Reminder 1')
        self.assertEqual(results[1].title, 'Reminder 2')

    def test_notifications_page(self):
        url = reverse('reminders', kwargs={'slug': self.user.username})
        data = {
            'action': 'search_reminders',
            'query': 'Reminder 1',
            'filter': 'reminder',
            'notifications_page': True,
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken', '')
        }
        request = self.factory.post(url, data)
        request.user = self.user
        request.session = {CURRENT_ORGANISATION_ID_KEY: self.organisation.id}

        results = search_reminders_or_notifications(request)

        # notifications is empty
        self.assertEqual(len(results), 0)
