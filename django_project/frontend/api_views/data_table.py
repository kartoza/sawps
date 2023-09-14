"""API Views related to data table.
"""
from django.db.models.query import QuerySet
from frontend.filters.data_table import DataContributorsFilter
from frontend.static_mapping import DATA_CONTRIBUTORS
from frontend.utils.data_table import data_table_reports
from frontend.utils.organisation import get_current_organisation_id
from property.models import Property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from stakeholder.models import UserProfile


class DataTableAPIView(APIView):
    """
    API view for retrieving data table reports.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        Get the filtered queryset based on user filters.
        """
        organisation_id = get_current_organisation_id(self.request.user)
        queryset = Property.objects.filter(
            organisation_id=organisation_id,
            ownedspecies__taxon__taxon_rank__name = "Species"
        ).order_by("name")

        filtered_queryset = DataContributorsFilter(
            self.request.GET, queryset=queryset
        ).qs

        return filtered_queryset

    def get(self, request) -> Response:
        """
        Handle GET request to retrieve data table reports.
        Params: request (Request) The HTTP request object.
        """
        queryset = self.get_queryset()
        id = self.request.user.id
        user_role = UserProfile.objects.get(user__id=id).user_role_type_id
        if user_role.name in DATA_CONTRIBUTORS:
            return Response(data_table_reports(queryset, request))
        else:
            return Response("")
