import logging
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
import pytz
from stakeholder.models import (
    Organisation,
    UserProfile,
    UserRoleType,
    UserTitle,
    Reminders
)
from django.contrib import messages
from stakeholder.tasks import send_reminder_email
from django.utils import timezone
from datetime import datetime
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
)
from django.http import JsonResponse
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
import json
from django.db.models import Q
from core.celery import app
from frontend.views.base_view import RegisteredOrganisationBaseView
from frontend.serializers.stakeholder import ReminderSerializer
logger = logging.getLogger(__name__)



class ProfileView(RegisteredOrganisationBaseView):
    template_name = 'profile.html'
    model = get_user_model()
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        if 'slug' not in kwargs:
            raise Http404('Missing username')

        profile = self.model.objects.get(username=kwargs['slug'])
        if profile != self.request.user:
            raise Http404('Mismatch user')

        if self.request.POST.get('first-name', ''):
            profile.first_name = self.request.POST.get('first-name', '')
        if self.request.POST.get('last-name', ''):
            profile.last_name = self.request.POST.get('last-name', '')

        if self.request.POST.get('email', ''):
            profile.email = self.request.POST.get('email', '')

        if not UserProfile.objects.filter(user=profile).exists():
            UserProfile.objects.create(
                user=profile,
            )

        if self.request.FILES.get('profile-picture', None):
            profile.user_profile.picture = self.request.FILES.get(
                'profile-picture', None
            )
        if self.request.POST.get('title', ''):
            title = UserTitle.objects.get(
                id=self.request.POST.get('title', ''))
            profile.user_profile.title_id = title
        if self.request.POST.get('role', ''):
            role = UserRoleType.objects.get(
                id=self.request.POST.get('role', '')
            )
            profile.user_profile.user_role_type_id = role

        profile.user_profile.save()
        profile.save()

        messages.success(
            request, 'Your changes have been saved.',
            extra_tags='notification'
        )

        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['titles'] = UserTitle.objects.all()
        context['roles'] = UserRoleType.objects.all()

        return context


def convert_reminder_dates(reminders):
    results = []
    for reminder in reminders:
        reminder.date = convert_date_to_local_time(
            reminder.date,
            reminder.timezone
        )
        results.append(reminder)

    return results


def search_reminders_or_notifications(request):
    search_query = request.POST.get('query')
    filter = request.POST.get('filter')
    notifications_page = request.POST.get('notifications_page')
    if filter is not None and filter != '':
        if filter == 'title':
            reminders = Reminders.objects.filter(
                Q(user=request.user),
                Q(organisation=request.session[CURRENT_ORGANISATION_ID_KEY]),
                Q(title__icontains=search_query)
            )
        else:
            reminders = Reminders.objects.filter(
                Q(user=request.user),
                Q(organisation=request.session[CURRENT_ORGANISATION_ID_KEY]),
                Q(reminder__icontains=search_query)
            )
    else:
        reminders = Reminders.objects.filter(
            Q(user=request.user),
            Q(organisation=request.session[CURRENT_ORGANISATION_ID_KEY]),
            Q(title__icontains=search_query) | Q(
                reminder__icontains=search_query)
        )
    if notifications_page is not None:
        notifications = []
        for reminder in reminders:
            if reminder.status == Reminders.PASSED and reminder.email_sent:
                notifications.append(reminder)
        return notifications
    else:
        return reminders


def delete_reminder_and_notification(request):
    data = json.loads(request.POST.get('ids'))
    notifications_page = request.POST.get('notifications_page')
    organisation = request.session[CURRENT_ORGANISATION_ID_KEY]
    try:
        for element in data:
            if isinstance(element, str) and element.isdigit():
                reminder = Reminders.objects.get(
                    user=request.user,
                    organisation=organisation,
                    id=int(element)
                )
                if reminder.user == request.user:
                    Reminders.objects.filter(
                        user=request.user,
                        organisation=organisation,
                        id=int(element)
                    ).delete()

        reminders = Reminders.objects.filter(
            user=request.user,
            organisation=organisation
        )
        if notifications_page is not None:
            notifications = []
            for reminder in reminders:
                if reminder.status == Reminders.PASSED and reminder.email_sent:
                    notifications.append(reminder)
            return notifications
        return reminders
    except Exception as e:
        return str(e)


def get_reminder_or_notification(request):
    data = json.loads(request.POST.get('ids'))

    try:
        for element in data:
            if isinstance(element, str) and element.isdigit():
                reminder = Reminders.objects.filter(
                    user=request.user,
                    organisation=request.session[CURRENT_ORGANISATION_ID_KEY],
                    id=int(element)
                )
                reminder[0].date = convert_date_to_local_time(
                    reminder[0].date,
                    reminder[0].timezone
                )

        return reminder
    except Exception as e:
        return str(e)


def paginate(*args):
    rows = args[0]
    rows_per_page = args[1]
    page = args[2]
    paginator = Paginator(rows, rows_per_page)

    try:
        paginated_rows = paginator.page(page)
    except PageNotAnInteger:
        paginated_rows = paginator.page(1)
    except EmptyPage:
        paginated_rows = paginator.page(paginator.num_pages)

    return paginated_rows


def get_organisation_reminders(request):

    reminders = Reminders.objects.filter(
        user=request.user,
        organisation=request.session[CURRENT_ORGANISATION_ID_KEY]
    )

    return reminders


def adjust_date_to_server_time(request):

    datetime_str = request.POST.get('date')
    timezone_value = request.POST.get('timezone')

    # Parse the date string into a datetime object
    datetime_format = '%Y-%m-%dT%H:%M'
    parsed_datetime = datetime.strptime(datetime_str, datetime_format)

    # timezone will be determined on the frontend
    local_timezone = pytz.timezone(timezone_value)
    local_datetime = local_timezone.localize(parsed_datetime)

    # Convert local datetime object to the server's timezone (UTC)
    server_timezone = timezone.get_current_timezone()
    server_datetime = local_datetime.astimezone(server_timezone)

    return server_datetime


def convert_date_to_local_time(date, timezone):
    # Convert the server time to the local timezone
    local_timezone = pytz.timezone(timezone)
    local_datetime = date.astimezone(local_timezone)

    # Convert the local datetime tothe desired format
    datetime_format = "%Y-%m-%d %I:%M %p"
    formatted_datetime = local_datetime.strftime(datetime_format)

    return formatted_datetime


class RemindersView(RegisteredOrganisationBaseView):
    template_name = 'reminders.html'
    model = get_user_model()
    slug_field = 'username'

    def get_reminders(self, request, **kwargs):

        reminders = get_organisation_reminders(request)

        reminders = convert_reminder_dates(reminders)

        new_reminders = ReminderSerializer(reminders, many=True)

        reminders_page = request.GET.get('reminders_page', 1)

        # Get the rows per page value from the query parameters
        rows_per_page = request.GET.get('reminders_per_page', 5)

        # paginate results
        paginated_rows = paginate(
            new_reminders.data,
            rows_per_page,
            reminders_page
        )

        return paginated_rows


    def add_reminder_and_schedule_task(self, request):
        if request.method == 'POST':
            title = request.POST.get('title')
            reminder_note = request.POST.get('reminder')
            adjusted_datetime = adjust_date_to_server_time(request)
            timezone_value = request.POST.get('timezone')

            if request.POST.get('reminder_type') == 'personal':
                reminder_type = Reminders.PERSONAL
            else:
                reminder_type = Reminders.EVERYONE
            try:
                organisation = Organisation.objects.get(
                    id=self.request.session[CURRENT_ORGANISATION_ID_KEY]
                )
                # Save the reminder to the database
                reminder = Reminders.objects.create(
                    user=request.user,
                    reminder = reminder_note,
                    title=title,
                    date=adjusted_datetime,
                    type = reminder_type,
                    organisation=organisation,
                    timezone=timezone_value
                )
                # Schedule the Celery task to send the reminder email
                task = send_reminder_email.apply_async(
                    args=[reminder.id],
                    eta=adjusted_datetime
                )
                task_id = task.id
                reminder.task_id = task_id
                reminder.save()

                reminders = get_organisation_reminders(request)
                reminders = convert_reminder_dates(reminders)
                serialized_reminders = ReminderSerializer(
                    reminders, many=True)

                return JsonResponse(
                    {
                        'status': 'success',
                        'updated_reminders': serialized_reminders.data
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': str(e)
                    }
                )


    def search_reminders(self, request):

        reminders = search_reminders_or_notifications(request)

        if isinstance(reminders, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': reminders
                }
            )

        reminders = convert_reminder_dates(reminders)

        search_results = ReminderSerializer(reminders, many=True)

        return JsonResponse({'data': search_results.data})


    def delete_reminder(self, request):

        new_reminders = delete_reminder_and_notification(request)

        if isinstance(new_reminders, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': new_reminders
                }
            )

        new_reminders = convert_reminder_dates(new_reminders)

        serialized_reminders = ReminderSerializer(
            new_reminders, many=True)

        return JsonResponse({'data': serialized_reminders.data})


    def get_reminder(self, request):

        reminder = get_reminder_or_notification(request)

        if isinstance(reminder, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': reminder
                }
            )

        reminder = convert_reminder_dates(reminder)

        result = ReminderSerializer(reminder, many=True)

        return JsonResponse({'data': result.data})

    def edit_reminder(self, request):
        data = json.loads(request.POST.get('ids'))
        title = request.POST.get('title')
        status = request.POST.get('status')
        adjusted_datetime = adjust_date_to_server_time(request)
        timezone_value = request.POST.get('timezone')
        type = request.POST.get('reminder_type')
        reminder_val = request.POST.get('reminder')
        email_sent = False
        cancel_task = False
        if type == 'personal':
            type = Reminders.PERSONAL
        else:
            type = Reminders.EVERYONE
        if status == 'active':
            status = Reminders.ACTIVE
            email_sent = False
        elif status == 'draft':
            status = Reminders.DRAFT
            email_sent = True
            cancel_task = True
        else:
            status = Reminders.PASSED
            email_sent = True
            cancel_task = True


        try:
            org = self.request.session[CURRENT_ORGANISATION_ID_KEY],
            for element in data:
                if isinstance(element, str) and element.isdigit():
                    reminder = Reminders.objects.get(
                        user=request.user,
                        organisation=org,
                        id=int(element)
                    )
                    if cancel_task:
                        app.control.revoke(reminder.task_id)


            reminder.title = title
            reminder.date = adjusted_datetime
            reminder.type = type
            reminder.status = status
            reminder.reminder = reminder_val
            reminder.email_sent = email_sent
            reminder.timezone = timezone_value
            reminder.save()

            reminders = get_organisation_reminders(request)
            serialized_reminders = ReminderSerializer(reminders, many=True)

            return JsonResponse({'data': serialized_reminders.data})
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'errors',
                    'message': str(e)
                }
            )


    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'get_reminders':
            return self.get_reminders(request)
        elif request.POST.get('action') == 'add_reminder':
            return self.add_reminder_and_schedule_task(request)
        elif request.POST.get('action') == 'search_reminders':
            return self.search_reminders(request)
        elif request.POST.get('action') == 'delete_reminder':
            return self.delete_reminder(request)
        elif request.POST.get('action') == 'get_reminder':
            return self.get_reminder(request)
        elif request.POST.get('action') == 'edit_reminder':
            return self.edit_reminder(request)
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(RemindersView, self).get_context_data(**kwargs)
        context['reminders'] = self.get_reminders(self.request)

        return context


class NotificationsView(RegisteredOrganisationBaseView):
    template_name = 'notifications.html'
    model = get_user_model()
    slug_field = 'username'

    def get_notifications(self, request):
        notifications = Reminders.objects.filter(
            user=request.user,
            organisation_id=request.session[CURRENT_ORGANISATION_ID_KEY],
            status=Reminders.PASSED,
            email_sent=True
        )
        new_notifications = convert_reminder_dates(notifications)
        serialized_notifications = ReminderSerializer(
            new_notifications, many=True)

        notifications_page = request.GET.get('notification_page', 1)

        # Get the rows per page value from the query parameters
        rows_per_page = request.GET.get('notifications_per_page', 5)

        # paginate results
        paginated_rows = paginate(
            serialized_notifications.data,
            rows_per_page, notifications_page
        )

        return paginated_rows


    def get_notification(self, request):

        notification = get_reminder_or_notification(request)

        if isinstance(notification, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': notification
                }
            )

        result = convert_reminder_dates(notification)

        serialized_notification = ReminderSerializer(result, many=True)

        return JsonResponse({'data': serialized_notification.data})


    def search_notifications(self, request):

        notifications = search_reminders_or_notifications(request)

        if isinstance(notifications, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': notifications
                }
            )

        search_results = convert_reminder_dates(notifications)

        serialized_notifications = ReminderSerializer(
            search_results, many=True)

        return JsonResponse({'data': serialized_notifications.data})


    def delete_notification(self, request):

        notifications = delete_reminder_and_notification(request)

        if isinstance(notifications, str):
            return JsonResponse(
                {
                    'status': 'error',
                    'message': notifications
                }
            )



        results = convert_reminder_dates(notifications)

        serialized_notifications = ReminderSerializer(results, many=True)

        return JsonResponse({'data': serialized_notifications.data})


    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'get_notification':
            return self.get_notification(request)
        elif request.POST.get('action') == 'search_notifications':
            return self.search_notifications(request)
        elif request.POST.get('action') == 'delete_notification':
            return self.delete_notification(request)
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context['notifications'] = self.get_notifications(self.request)

        return context
