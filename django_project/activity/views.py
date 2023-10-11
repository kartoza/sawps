from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from activity.models import ActivityType
from rest_framework.response import Response


class ActivityTypeAPIView(APIView):
    """Get Activity Type"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ActivityType.get_all_activities()
        return Response(
            status=200,
            data=queryset
        )
