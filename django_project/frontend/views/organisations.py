from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from core.settings.contrib import SUPPORT_EMAIL
from .base_view import RegisteredOrganisationBaseView
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

        use_of_data_changes = []

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

            if organisation.use_of_data_by_sanbi_only != only_sanbi:
                use_of_data_changes.append(
                    f'Use of data by SANBI only changed from '
                    f'{organisation.use_of_data_by_sanbi_only} '
                    f'to {only_sanbi}.'
                )
            organisation.use_of_data_by_sanbi_only = (
                only_sanbi
            )

            if (
                organisation.hosting_through_sanbi_platforms !=
                hosting_data_sanbi
            ):
                use_of_data_changes.append(
                    f'Hosting / serving the data through SANBI '
                    f'platforms and portals changed from '
                    f'{organisation.hosting_through_sanbi_platforms} '
                    f'to {hosting_data_sanbi}.'
                )
            organisation.hosting_through_sanbi_platforms = (
                hosting_data_sanbi
            )

            if (
                organisation.allowing_sanbi_to_expose_data !=
                hosting_data_sanbi_other
            ):
                use_of_data_changes.append(
                    f'Hosting through SANBI and allowing SANBI '
                    f'to publish the Data '
                    f'to other portals, as well as to actively '
                    f'curate the data changed from '
                    f'{organisation.allowing_sanbi_to_expose_data} '
                    f'to {hosting_data_sanbi_other}.'
                )
            organisation.allowing_sanbi_to_expose_data = (
                hosting_data_sanbi_other
            )

            organisation.save()

            messages.success(
                request, 'Your changes have been saved.',
                extra_tags='notification'
            )

            if len(use_of_data_changes) > 0:
                changes_list_html = "".join(
                    [f"<li>{change}</li>" for change in use_of_data_changes])
                subject = (
                    f'SAWPS Organisation - '
                    f'Changes to {organisation.name}\'s Permissions Settings'
                )
                message = render_to_string(
                    'emails/organisation_permission_changed.html',
                    {
                        'organisation': organisation.name,
                        'support_email': SUPPORT_EMAIL,
                        'changes_list': changes_list_html
                    }
                )
                send_mail(
                    subject,
                    None,
                    settings.SERVER_EMAIL,
                    list(User.objects.filter(
                        is_superuser=True
                    ).values_list('email', flat=True)),
                    html_message=message
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
