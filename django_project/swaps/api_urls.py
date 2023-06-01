from django.urls import path
from swaps.api_views.reminder import (
    ReminderDetail,
    ReminderList
)


urlpatterns = [
    path('reminder/', ReminderDetail.as_view(), name='get-reminder'),
    path('reminders/',ReminderList.as_view(), name='list-reminder'),
]
