import json
from stakeholder.request_context import set_request
from stakeholder.models import (
    OrganisationInvites, 
    OrganisationUser,
    UserProfile,
    UserRoleType
)
from django.contrib.auth.models import User
from .base_view import RegisteredOrganisationBaseView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views.generic import TemplateView
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
)
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import models



class OrganisationUsersView(
    LoginRequiredMixin, RegisteredOrganisationBaseView, TemplateView):
    """
    OrganisationUsersView displays the organisations
    users page by rendering the 'users.html' template.
    """
    template_name = 'users.html'
    model = OrganisationUser
    context_object_name = 'organisation_users'


    def extract_substring(self, string):
        '''extract search string from search box on frontend'''
        if len(string) >= 2:
            if '=' in string:
                substring = string.split('=')[1]
                return substring
            else:
                return string

    def search_users(self, username):
        users = User.objects.filter(username__icontains=username)
        return users

    def get_user_email(self, user):
        try:
            user = User.objects.get(username=user)
            return user.email
        except User.DoesNotExist:
            return None

    def get_user_role(self, role):
        try:
            role = UserRoleType.objects.get(name=role)
            return role
        except UserRoleType.DoesNotExist:
            return None

    def get_user_role_by_user(self, user):
        try:
            role = UserProfile.objects.get(user=user)
            return str(role.user_role_type_id)
        except UserProfile.DoesNotExist:
            return None

    def is_new_invitation(self, email, organisation):
        """
        Check if an entry with the given email and 
        organisation already exists.
        Returns True if exists, False otherwise.
        """
    
        try:
            invitation = OrganisationInvites.objects.filter(
                email=email,
                organisation_id=organisation
            ).first()                
            if invitation:
                return invitation.joined
            else: return False
        except OrganisationInvites.DoesNotExist:
            return None


    def calculate_rows_per_page(self, data):
        total_rows = len(data)

        desired_rows_per_page = 5

        # Calculate the dynamic number of rows per page
        rows_per_page = min(desired_rows_per_page, total_rows)

        return rows_per_page


    def search_table(self, request):
        query = request.POST.get('query')
        extracted_string = self.extract_substring(query)
        matching_users = self.search_users(extracted_string)

        data = []

        # search user within the orginisation
        for user in matching_users:
            try:
                org_user = OrganisationUser.objects.get(user=user)
                role = UserProfile.objects.get(user=user).user_role_type_id
                role = str(role)
            except OrganisationUser.DoesNotExist:
                continue
            except UserProfile.DoesNotExist:
                role = None
            if org_user:
                if not org_user.user == self.request.user:
                    data.append({
                        'organisation': str(org_user.organisation),
                        'user': str(org_user.user),
                        'id': org_user.user.id,
                        'role': role
                        # Add more columns as needed
                    })

        return JsonResponse({'data': json.dumps(data, cls=DjangoJSONEncoder)})

    def post(self, request):
        # Default post method logic
        return JsonResponse({'status': 'success'})

    def invite_post(self, request):

        # retrieve data from front end/html template
        email = request.POST.get('email')
        role = request.POST.get('inviteAs')
        permissions = request.POST.get('memberRole')

        # assign role from the roles defined in the db
        if role == 'manager':
            if permissions == 'write':
                role = 'Admin'
            else:
                role = 'Base user'
        else:
            if permissions == 'write':
                role = 'Admin'
            else:
                role = 'Base user'

        # get role by name
        user_role = self.get_user_role(role)

        try:
            # add invitation to model
            is_new_invitation = self.is_new_invitation(
                email, self.request.session[CURRENT_ORGANISATION_ID_KEY])
            org_id = self.request.session[CURRENT_ORGANISATION_ID_KEY]
            if not is_new_invitation:
                if role == 'manager':
                    create_invite = OrganisationInvites(
                        email=email,
                        organisation_id=org_id,
                        user_role=user_role,
                        assigned_as=OrganisationInvites.MANAGER
                    )
                else:
                    create_invite = OrganisationInvites(
                        email=email,
                        organisation_id=org_id,
                        user_role=user_role,
                        assigned_as=OrganisationInvites.MEMBER
                    )


                set_request(request)  # Set the request object
                create_invite.save()
                
                invites = self.get_organisation_invites()
                serialized_invites = json.dumps(list(invites))
                return JsonResponse(
                    {
                        'status': 'success',
                        'updated_invites': serialized_invites
                    }
                )
            else:
                return JsonResponse({'status': 'invitation already sent'})
        except Exception as e:
            print(f"Error creating invite: {str(e)}")
            return JsonResponse({'status': 'invitation already sent'})




    def delete_post(self, request):
        object_id = request.POST.get('object_id')
        try:
            user = models.User.objects.get(pk=object_id)
            organisation = OrganisationUser.objects.get(user=object_id)
            org_invite = OrganisationInvites.objects.get(
                email=user.email, organisation=organisation.organisation)
            org_invite.joined = False
            org_invite.save()
            OrganisationUser.objects.filter(user=object_id).delete()
            return JsonResponse({'status': 'success'})
        except models.User.DoesNotExist:
            return JsonResponse({'status': 'failed'})
        except OrganisationUser.DoesNotExist:
            return JsonResponse({'status': 'failed'})
        except OrganisationInvites.DoesNotExist:
            return JsonResponse({'status': 'failed'})

        
        


    def get_organisation_users(self):
        organisation_user_list = OrganisationUser.objects.filter(
            organisation_id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
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
        organisation_invites = OrganisationInvites.objects.filter(
            organisation_id=self.request.session[CURRENT_ORGANISATION_ID_KEY])
        paginated_organisation_invites = []

        for invite in organisation_invites:
            object_to_save = {
                "pk": invite.pk,
                "email": str(invite.email),
                "user_role": str(invite.user_role),
                "joined": invite.joined
            }
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

    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'invite':
            return self.invite_post(request)
        elif request.POST.get('action') == 'delete':
            return self.delete_post(request)
        elif request.POST.get('action') == 'search_table':
            return self.search_table(request)
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['users'] = self.get_organisation_users()
        ctx['invites'] = self.get_organisation_invites()
        ctx['role'] = self.get_user_role_by_user(self.request.user)
        return ctx
