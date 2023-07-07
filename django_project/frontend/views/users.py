
from stakeholder.models import OrganisationUser, UserProfile
from .base_view import RegisteredOrganisationBaseView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views.generic import TemplateView
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class OrganisationUsersView(LoginRequiredMixin,RegisteredOrganisationBaseView,TemplateView):
    """
    OrganisationUsersView displays the organisations users page by rendering the 'users.html' template.
    """
    template_name = 'users.html'
    model = OrganisationUser
    context_object_name = 'organisation_users'
    
    def post(self, request):
        # Default post method logic
        return JsonResponse({'status': 'success'})
    
    def delete_post(self,request):
        object_id = request.POST.get('object_id')
        OrganisationUser.objects.filter(user=object_id).delete()

        return JsonResponse({'status': 'success'})
    
    def create_post(self,request):
        # this one will be used for adding members invites and all

        return JsonResponse({'status': 'success'})
    
    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('action') == 'create':
            return self.create_post(request)
        elif request.POST.get('action') == 'delete':
            return self.delete_post(request)
        else:
            return super().dispatch(request, *args, **kwargs)
        

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
        ctx['users'] = self.get_organisation_users()
        ctx['invites'] = self.get_organisation_invites()
        return ctx

