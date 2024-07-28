"""API Views related to data table.
"""
from typing import List

from django.db.models.query import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.static_mapping import (
    DATA_CONSUMERS,
    PROVINCIAL_DATA_CONSUMER
)
from frontend.utils.data_table import (
    get_param_from_request,
    data_table_reports,
    national_level_user_table,
    national_level_province_report,
    national_level_property_report,
    national_level_activity_report,
    national_level_species_report,
    PROVINCE_REPORT,
    PROPERTY_REPORT,
    ACTIVITY_REPORT,
    SPECIES_REPORT,
    write_report_to_rows,
    get_queryset,
    get_taxon_queryset
)
from frontend.utils.user_roles import get_user_roles


class DataTableAPIView(APIView):
    """
    API view for retrieving data table reports.
    """
    permission_classes = [IsAuthenticated]

    def get_taxon_queryset(self):
        """
        Get the filtered Taxon queryset based on user filters.
        """
        return get_taxon_queryset(self.request)

    def get_queryset(self, user_roles: List[str]) -> QuerySet:
        """
        Get the filtered queryset based on user filters.
        """
        return get_queryset(user_roles, self.request)

    def process_request(self, request) -> Response:
        """
        Handle request to retrieve data table reports.
        Params: request (Request) The HTTP request object.
        """

        user_roles = get_user_roles(self.request.user)
        queryset = self.get_queryset(user_roles)
        if self.get_taxon_queryset().count() == 0:
            return Response(status=200, data=[])
        show_detail = self.request.user.is_superuser \
            or not set(user_roles) & set(DATA_CONSUMERS)
        if show_detail:
            if get_param_from_request(request, "file"):
                return Response({
                    "file": write_report_to_rows(queryset, request)
                })

            reports = data_table_reports(queryset, request, user_roles)
            report_list = get_param_from_request(request, "reports", None)
            if report_list:
                report_list = report_list.split(",")
                if PROVINCE_REPORT in report_list:
                    taxon_queryset = self.get_taxon_queryset()
                    province_reports = national_level_province_report(
                        taxon_queryset,
                        request
                    )
                    if province_reports:
                        reports.append({
                            PROVINCE_REPORT: province_reports
                        })

            return Response(reports)

        else:
            if get_param_from_request(request, "file"):
                report_functions = {
                    PROPERTY_REPORT: national_level_property_report,
                    ACTIVITY_REPORT: national_level_activity_report,
                    SPECIES_REPORT: national_level_species_report,
                }

                if PROVINCIAL_DATA_CONSUMER not in user_roles:
                    report_functions[
                        PROVINCE_REPORT
                    ] = national_level_province_report
                return Response({
                    "file": write_report_to_rows(
                        queryset, request, report_functions
                    )
                })
            return Response(
                national_level_user_table(
                    queryset, request)
            )


    def get(self, request) -> Response:
        """
        Handle GET request to retrieve data table reports.
        Params: request (Request) The HTTP request object.
        """
        return self.process_request(request)

    def post(self, request) -> Response:
        """
        Handle POST request to retrieve data table reports.
        Params: request (Request) The HTTP request object.
        """
        return self.process_request(request)
