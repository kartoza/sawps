
from stakeholder.models import OrganisationUser
from .base_view import RegisteredOrganisationBaseView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views.generic import TemplateView


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
