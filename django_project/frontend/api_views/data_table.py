"""API Views related to data table.
"""
from typing import List

from django.db.models.query import QuerySet
from frontend.filters.data_table import DataContributorsFilter
from frontend.filters.metrics import BaseMetricsFilter
from frontend.static_mapping import (
    DATA_CONTRIBUTORS,
    DATA_SCIENTISTS
)
from frontend.utils.data_table import (
    data_table_reports,
    national_level_user_table
)
from frontend.utils.organisation import get_current_organisation_id
from property.models import Property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from species.models import Taxon


class DataTableAPIView(APIView):
    """
    API view for retrieving data table reports.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user_roles: List[str]) -> QuerySet:
        """
        Get the filtered queryset based on user filters.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        if set(user_roles) & set(DATA_CONTRIBUTORS + DATA_SCIENTISTS):
            query_filter = DataContributorsFilter
            organisation = self.request.GET.get("organisation")
            if organisation and (set(user_roles) & set(DATA_SCIENTISTS)):
                ids = organisation.split(",")
                queryset = Property.objects.filter(
                    organisation_id__in=ids,
                    ownedspecies__taxon__taxon_rank__name="Species"
                )
            else:
                queryset = Property.objects.filter(
                    organisation_id=organisation_id,
                    ownedspecies__taxon__taxon_rank__name="Species"
                ).order_by("name")
        else:
            query_filter = BaseMetricsFilter
            queryset = Taxon.objects.filter(
                ownedspecies__property__organisation_id=organisation_id,
                taxon_rank__name="Species"
            ).distinct()

        filtered_queryset = query_filter(
            self.request.GET, queryset=queryset
        ).qs

        return filtered_queryset

    def get(self, request) -> Response:
        """
        Handle GET request to retrieve data table reports.
        Params: request (Request) The HTTP request object.
        """
        user_roles = list(
            self.request.user.groups.all().values_list(
                'name', flat=True
            )
        )
        queryset = self.get_queryset(user_roles)

        if set(user_roles) & set(DATA_CONTRIBUTORS + DATA_SCIENTISTS):
            return Response(data_table_reports(queryset, request))

        else:
            return Response(
                national_level_user_table(
                    queryset, request, user_roles)
            )
