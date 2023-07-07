"""Provide classes for base view."""
from django.views.generic import TemplateView
from stakeholder.models import OrganisationUser, Organisation, UserProfile
from frontend.serializers.stakeholder import OrganisationSerializer, OrganisationUsersSerializer
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
    CURRENT_ORGANISATION_KEY
)

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class RegisteredOrganisationBaseView(TemplateView):
    """
    Base view to provide organisation context for logged-in users.
    """
    def set_current_organisation(self, organisation: Organisation):
        if organisation:
            self.request.session[
                CURRENT_ORGANISATION_ID_KEY] = organisation.id
            self.request.session[
                CURRENT_ORGANISATION_KEY] = organisation.name
        else:
            self.request.session[
                CURRENT_ORGANISATION_ID_KEY] = 0
            self.request.session[
                CURRENT_ORGANISATION_KEY] = ''
    

    def get_or_set_current_organisation(self):
        if (
            CURRENT_ORGANISATION_ID_KEY in self.request.session and
            CURRENT_ORGANISATION_KEY in self.request.session
        ):
            return (
                self.request.session[CURRENT_ORGANISATION_ID_KEY],
                self.request.session[CURRENT_ORGANISATION_KEY]
            )
        organisation: Organisation = None
        if self.request.user.is_superuser:
            organisation = Organisation.objects.all().order_by('name').first()
        else:
            organisation_user = OrganisationUser.objects.filter(
                user=self.request.user
            ).select_related('organisation').order_by(
                'organisation__name'
            ).first()
            if organisation_user:
                organisation = organisation_user.organisation
        self.set_current_organisation(organisation)
        return (
            organisation.id, organisation.name
        ) if organisation else (0, '')

    def get_organisation_list(self):
        if self.request.user.is_superuser:
            # fetch all organisations
            organisations = Organisation.objects.all().order_by('name')
            if CURRENT_ORGANISATION_ID_KEY in self.request.session:
                organisations = organisations.exclude(
                    id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
            return OrganisationSerializer(organisations, many=True).data
        # non-superuser organisations
        user_organisations = OrganisationUser.objects.filter(
            user=self.request.user
        ).order_by('organisation_id').values_list(
            'organisation_id', flat=True
        ).distinct()
        organisations = Organisation.objects.filter(
            id__in=user_organisations
        ).order_by('name')
        if CURRENT_ORGANISATION_ID_KEY in self.request.session:
            organisations = organisations.exclude(
                id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
        return OrganisationSerializer(organisations, many=True).data
    
    

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    def get_organisation_users(self):
        organisation_user_list = OrganisationUser.objects.filter(organisation_id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
        organisation_users = []

        for user in organisation_user_list:
            role = UserProfile.objects.all().filter(user=user.user.id).first()
            if role:
                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": str(user.user),
                    "role": role.user_role_type_id.name,
                }
            else:
                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": str(user.user),
                    "role": None,
                }
            if not user.user == self.request.user:
                organisation_users.append(object_to_save)

        users_page = self.request.GET.get('users_page', 1)
        
        # Get the rows per page value from the query parameters
        rows_per_page = self.request.GET.get('users_per_page', 3)
        
        paginator = Paginator(organisation_users, rows_per_page)
        
        try:
            users = paginator.page(users_page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        return users

    def get_organisation_invites(self):
        organisation_invites = OrganisationUser.objects.filter(organisation_id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
        paginated_organisation_invites = []

        for user in organisation_invites:
            role = UserProfile.objects.all().filter(user=user.user.id).first()
            if role:
                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": str(user.user),
                    "role": role.user_role_type_id.name
                }
            else:
                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": str(user.user),
                    "role": None,
                }
            if not user.user == self.request.user:
                paginated_organisation_invites.append(object_to_save)

        invites_page = self.request.GET.get('invites_page', 1)
        
        # Get the rows per page value from the query parameters
        rows_per_page = self.request.GET.get('invites_per_page', 5)
        
        paginator = Paginator(paginated_organisation_invites, rows_per_page)
        
        try:
            invites = paginator.page(invites_page)
        except PageNotAnInteger:
            invites = paginator.page(1)
        except EmptyPage:
            invites = paginator.page(paginator.num_pages)
        
        return invites



    def calculate_rows_per_page(self, data):
        total_rows = len(data)
        
        # Define the desired number of rows per page based on your logic
        desired_rows_per_page = 5
        
        # Calculate the dynamic number of rows per page
        rows_per_page = min(desired_rows_per_page, total_rows)
        
        return rows_per_page


    


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return ctx
        current_organisation_id, current_organisation = (
            self.get_or_set_current_organisation()
        )
        # fetch organisation list
        ctx['current_organisation'] = (
            current_organisation if current_organisation else '-'
        )
        ctx['current_organisation_id'] = current_organisation_id
        ctx['organisations'] = self.get_organisation_list()
        ctx['users'] = self.get_organisation_users()
        ctx['invites'] = self.get_organisation_invites()
        return ctx
