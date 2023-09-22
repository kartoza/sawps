from .base_view import RegisteredOrganisationBaseView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stakeholder.models import Organisation
from frontend.serializers.stakeholder import (
    OrganisationSerializer
)
from django.http import JsonResponse
from django.contrib import messages



def save_permissions(request, organisation_id):
    if request.method == 'POST':
        only_sanbi_str = request.POST.get('only_sanbi')
        hosting_data_sanbi_str = request.POST.get(
            'hosting_data_sanbi'
        )
        hosting_data_sanbi_other_str = request.POST.get(
            'hosting_data_sanbi_other'
        )

        only_sanbi = only_sanbi_str.lower() == 'true'
        hosting_data_sanbi = (
            hosting_data_sanbi_str.lower() == 'true'
        )
        hosting_data_sanbi_other = (
            hosting_data_sanbi_other_str.lower() == 'true'
        )

        try:
            organisation = Organisation.objects.get(
                pk=organisation_id
            )

            organisation.use_of_data_by_sanbi_only = (
                only_sanbi
            )
            organisation.hosting_through_sanbi_platforms = (
                hosting_data_sanbi
            )
            organisation.allowing_sanbi_to_expose_data = (
                hosting_data_sanbi_other
            )

            organisation.save()

            messages.success(
                request, 'Your changes have been saved.',
                extra_tags='notification'
            )

            return JsonResponse(
                {'message': 'Permissions saved successfully'}
            )
        except Organisation.DoesNotExist:
            return JsonResponse(
                {'error': 'Organization not found'},
                status=404
            )

    return JsonResponse(
        {'error': 'Invalid request'},
        status=400
    )


@api_view(['GET'])
def organization_detail(request, identifier):
    organization = get_object_or_404(
        Organisation,
        id=identifier
    )
    serializer = OrganisationSerializer(organization)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


class OrganisationsView(
    LoginRequiredMixin,
    RegisteredOrganisationBaseView,
    TemplateView
):
    """
    OrganisationsView displays the organisations the
    user can access.
    """
    template_name = 'organisations.html'
    context_object_name = 'organisations'


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
