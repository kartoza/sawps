import json
import uuid
from django.db.models import Value as V, Q
from django.db.models.functions import Concat

from sawps.views import AddUserToOrganisation
from stakeholder.models import (
    Organisation,
    OrganisationInvites,
    OrganisationUser,
    OrganisationRepresentative,
    UserProfile,
    UserRoleType, MANAGER, MEMBER
)
from django.contrib.auth.models import User
from .base_view import RegisteredOrganisationBaseView

from django.http import JsonResponse

from django.views.generic import TemplateView
from frontend.utils.organisation import (
    get_current_organisation_id
)
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import models
from django.contrib.sites.models import Site
from urllib.parse import quote


class OrganisationUsersView(
    RegisteredOrganisationBaseView,
    TemplateView
):
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
        return string

    def search_users(self, username):
        users = User.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=username) | Q(username__icontains=username)
        )
        return users

    def get_user_email(self, user):
        try:
            user = User.objects.get(username=user)
            return user.email
        except User.DoesNotExist:
            return None

    def get_user_role(self, role):
        try:
            role = UserRoleType.objects.filter(
                name__icontains=role
            ).first()
            return role
        except UserRoleType.DoesNotExist:
            return None


    def get_role(self, user, organisation):
        current_user = OrganisationInvites.objects.filter(
            email=user.email,
            organisation_id=organisation
        ).first()
        if current_user:
            return current_user.user_role
        else:
            role = UserProfile.objects.filter(user=user).first()
            if role:
                return role.user_role_type_id

    def is_new_invitation(self, email, organisation):
        """
        Check if an entry with the given email and
        organisation already exists.
        Returns True if exists, False otherwise.
        """

        invitation = OrganisationInvites.objects.filter(
            email=email,
            organisation_id=organisation
        ).first()

        if invitation:
            return True
        return False

    def is_user_registered(self, email):
        user = User.objects.filter(email=email).first()
        if user:
            return (True, user)
        else:
            return (False, None)


    def calculate_rows_per_page(self, data):
        total_rows = len(data)

        desired_rows_per_page = 5

        # Calculate the dynamic number of rows per page
        rows_per_page = min(desired_rows_per_page, total_rows)

        return rows_per_page

    def search_user_table(self, request):
        query = request.POST.get('query')
        organisation = request.POST.get('current_organisation')
        extracted_string = self.extract_substring(query)
        matching_users = self.search_users(extracted_string)

        data = []

        # search user within the orginisation
        for user in matching_users:
            try:
                org = Organisation.objects.get(name=str(organisation))
                org_user = OrganisationUser.objects.get(
                    user=user,
                    organisation=org)
                invite = OrganisationInvites.objects.filter(
                    email=user.email,
                    organisation_id=org.id
                ).first()
            except Organisation.DoesNotExist:
                org = None
                org_user = None
            except OrganisationUser.DoesNotExist:
                org_user = None
            if org_user:
                if not org_user.user == self.request.user and invite:
                    data.append({
                        'organisation': str(org_user.organisation),
                        'user': org_user.user.get_full_name(),
                        'id': org_user.user.id,
                        'role': 'Organisation ' + invite.assigned_as,
                        'joined': invite.joined
                    })

        return JsonResponse(
            {
                'data': json.dumps(data, cls=DjangoJSONEncoder)
            }
        )

    def post(self, request):
        # Default post method logic
        return JsonResponse({'status': 'success'})

    def invite_post(self, request):
        # retrieve data from front end/html template
        email = request.POST.get('email')
        assign_as = request.POST.get('inviteAs')
        # assign role as base user
        role = 'Base user'
        # get role by name
        user_role = self.get_user_role(role)
        try:
            # add invitation to model
            is_new_invitation = self.is_new_invitation(
                email,
                get_current_organisation_id(request.user)
            )
            org_id = get_current_organisation_id(request.user)
            if not is_new_invitation:
                organisation = Organisation.objects.get(id=org_id)

                # assert if user is registered on platform
                registered, user = self.is_user_registered(email)
                invitation_uuid = uuid.uuid4().hex
                if registered:
                    return_url = (
                        Site.objects.get_current().domain +
                        f'/adduser/{invitation_uuid}/'
                    )
                else:
                    encoded_email = quote(email, safe='')
                    return_url = (
                        Site.objects.get_current().domain +
                        '/accounts/signup/?email=' + encoded_email +
                        '&uuid=' + quote(invitation_uuid)
                    )

                create_invite = OrganisationInvites(
                    email=email,
                    organisation_id=org_id,
                    user_role=user_role,
                    assigned_as=MANAGER if assign_as == 'manager' else MEMBER,
                    user=user,
                    uuid=invitation_uuid
                )

                # object to pass to view function
                email_details = {
                    'return_url': return_url,
                    'user': {
                        'role': request.POST.get('inviteAs'),
                        'organisation': organisation.name
                    },
                    'support_email': request.user.email,
                    'recipient_email': email,
                    'domain': Site.objects.get_current().domain
                }

                # instantiate the view
                add_user_view = AddUserToOrganisation()
                if add_user_view.send_invitation_email(email_details):
                    create_invite.save()
                    invites = self.get_organisation_invites(request)
                    serialized_invites = json.dumps(list(invites))
                    return JsonResponse(
                        {
                            'status': 'success',
                            'updated_invites': serialized_invites,
                            'number': invites.number,
                            'previous_page_number': (
                                invites.previous_page_number() if
                                invites.has_previous() else -1
                            ),
                            'next_page_number': (
                                invites.next_page_number() if
                                invites.has_next() else -1
                            ),
                            'per_page': invites.paginator.per_page
                        }
                    )
                return JsonResponse({
                    'status': 'Failed to send email'
                })
            else:
                return JsonResponse({
                    'status': 'Invitation already sent'
                })
        except Organisation.DoesNotExist:
            return JsonResponse({
                'status': 'Organisation does not exist'
            })
        except Exception as e:
            return JsonResponse({
                'status': str(e)
            })

    def delete_post(self, request):
        object_id = request.POST.get('object_id')
        current_organisation = request.POST.get('current_organisation')
        try:
            current_organisation = Organisation.objects.get(
                name=str(current_organisation))
            user = models.User.objects.get(pk=object_id)
            OrganisationInvites.objects.filter(
                Q(email=user.email) | Q(user=object_id),
                organisation=current_organisation
            ).delete()
            OrganisationUser.objects.filter(
                user=object_id,
                organisation=current_organisation
            ).delete()
            return JsonResponse({'status': 'success'})
        except Organisation.DoesNotExist:
            return JsonResponse({'status': 'failed'})
        except models.User.DoesNotExist:
            return JsonResponse({'status': 'failed'})
        except Exception:
            # when deletion fails
            return JsonResponse({'status': 'failed'})

    def get_organisation_users(self, request):
        # Get manager
        organisation_reps_list = OrganisationRepresentative.objects.filter(
            organisation_id=get_current_organisation_id(request.user)
        )
        organisation_users = []
        for user in organisation_reps_list:
            object_to_save = {
                "id": user.user.id,
                "organisation_user": user.user.get_full_name(),
                "role": MANAGER,
                "assigned_as": MANAGER,
                "joined": True
            }
            organisation_users.append(object_to_save)

        # Get member
        organisation_user_list = OrganisationUser.objects.filter(
            organisation_id=get_current_organisation_id(request.user)
        ).exclude(
            user__in=[uid.user for uid in organisation_reps_list]
        )

        for user in organisation_user_list:
            # get role from organisation invites
            role = OrganisationInvites.objects.filter(
                email=user.user.email,
                organisation_id=(
                    get_current_organisation_id(request.user)
                )
            ).first()
            if role:
                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": user.user.get_full_name(),
                    "role": role.user_role,
                    "assigned_as": role.assigned_as,
                    "joined": role.joined
                }
            else:
                assigned_as = MEMBER
                if hasattr(user.user, 'user_profile'):
                    user_profile = user.user.user_profile
                    role = str(user_profile.user_role_type_id)
                    if role == 'Admin' or role == 'Super User':
                        assigned_as = MANAGER

                object_to_save = {
                    "id": user.user.id,
                    "organisation_user": user.user.get_full_name(),
                    "role": None,
                    "assigned_as": assigned_as,
                    "joined": True
                }

            organisation_users.append(object_to_save)

        users_page = request.GET.get('users_page', 1)

        # Get the rows per page value from the query parameters
        rows_per_page = request.GET.get('users_per_page', 5)

        paginator = Paginator(organisation_users, rows_per_page)

        try:
            users = paginator.page(users_page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return users

    def get_organisation_invites(self, request):
        organisation_invites = OrganisationInvites.objects.filter(
            organisation_id=get_current_organisation_id(request.user)
        ).order_by('-id')
        paginated_organisation_invites = []

        for invite in organisation_invites:
            object_to_save = {
                "pk": invite.pk,
                "email": str(invite.email),
                "user_role": str(invite.assigned_as),
                "assigned_as": str(invite.assigned_as),
                "joined": invite.joined
            }
            paginated_organisation_invites.append(object_to_save)

        invites_page = request.GET.get('invites_page', 1)

        # Get the rows per page value from the query parameters
        rows_per_page = request.GET.get('invites_per_page', 5)

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
        elif request.POST.get('action') == 'search_user_table':
            return self.search_user_table(request)
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['users'] = self.get_organisation_users(self.request)
        ctx['invites'] = self.get_organisation_invites(self.request)
        ctx['role'] = self.get_role(
            self.request.user,
            get_current_organisation_id(self.request.user))
        return ctx
