# -*- coding: utf-8 -*-


"""API view for reminder.
"""
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from notification.models import Reminder
from notification.serializers.reminder import ReminderSerializer


class ReminderDetail(APIView):
    """Return a reminder"""

    def get_object(self, pk):
        try:
            return Reminder.objects.get(pk=pk)
        except Reminder.DoesNotExist:
            raise Http404

    def get(self, request):
        reminder_id = request.GET.get('reminderId')
        reminder = self.get_object(reminder_id)
        serializer = ReminderSerializer(reminder)
        data = serializer.data

        return Response(data)


class ReminderList(APIView):
    """Return list of reminder"""

    def get(self, request):
        status = request.GET.get('status')
        reminders = Reminder.objects.all()
        if status:
            reminders = Reminder.objects.filter(status=status)

        serializer = ReminderSerializer(reminders, many=True)

        return Response(serializer.data)
