from django.http import JsonResponse
from django.views.generic import TemplateView
from stakeholder.models import (
    OrganisationUser,
    Organisation,
    Reminders,
    UserProfile
)
from frontend.serializers.stakeholder import (
    OrganisationSerializer
)
from django.contrib import messages
from datetime import datetime


def get_user_notifications(request):
    """Method checks if there are new notifications
    to send the user, these notifications are
    updated from stakeholder.tasks."""
    current_date = datetime.now().date()
    reminders = Reminders.objects.filter(
        user=request.user.id,  # Use the user ID instead of the object
        status=Reminders.PASSED,
        email_sent=True,
        date__date=current_date
    )
    notifications = []
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.received_notif:
            for reminder in reminders:
                messages.success(
                    request,
                    reminder.title,
                    extra_tags='notification'
                )
                notifications.append(reminder.title)
        if len(notifications) > 0:
            user_profile.received_notif = True
            user_profile.save()
        return JsonResponse(
            {
                'status': 'success',
                'user_notifications': notifications
            }
        )
    except Exception:
        return JsonResponse(
            {
                'status': 'error',
                'user_notifications': []
            }
        )



class RegisteredOrganisationBaseView(TemplateView):
    """
    Base view to provide organisation context for logged-in users.
    """

    def get_current_organisation(self):
        user = self.request.user
        user_profile = user.user_profile
        current_organisation = (
            user_profile.current_organisation
            if user_profile else None
        )
        return current_organisation


    def get_or_set_current_organisation(self, request):
        user = request.user

        user_profile = user.user_profile
        current_organisation = user_profile.current_organisation

        if current_organisation:
            return current_organisation.id, current_organisation.name

        organisation = None

        if user.is_superuser:
            organisation = (
                Organisation.objects.all().order_by('name').first()
            )
        else:
            organisation_user = OrganisationUser.objects.filter(
                user=user
            ).select_related('organisation').order_by(
                'organisation__name'
            ).first()
            if organisation_user:
                organisation = organisation_user.organisation

        if organisation:
            # Set the current organization in the user's profile
            user_profile.current_organisation = organisation
            user_profile.save()
            return organisation.id, organisation.name

        return 0, ''


    def get_organisation_list(self, request):
        user = request.user
        user_profile = user.user_profile
        if user.is_superuser:
            organisations = (
                Organisation.objects.all().order_by('name')
            )
            if user_profile.current_organisation:
                organisations = organisations.exclude(
                    id=user_profile.current_organisation.id
                )
        else:
            user_organisations = OrganisationUser.objects.filter(
                user=user
            ).order_by('organisation_id')
            if user_profile.current_organisation:
                user_organisations = user_organisations.exclude(
                    id=user_profile.current_organisation.id
                )
            organisations = (
                [org_user.organisation for org_user in user_organisations]
            )

        return OrganisationSerializer(organisations, many=True).data


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return ctx
        current_organisation_id, current_organisation = (
            self.get_or_set_current_organisation(self.request)
        )
        # fetch organisation list
        ctx['current_organisation'] = (
            current_organisation if current_organisation else '-'
        )
        ctx['current_organisation_id'] = current_organisation_id
        ctx['organisations'] = self.get_organisation_list(self.request)
        get_user_notifications(self.request)
        return ctx
