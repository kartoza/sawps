from django.contrib import admin

from swaps.models import Reminder

# Register your models here.


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'text', 'status')
    list_filter = ('title','status', 'date')
    ordering = ('status', 'date')


admin.site.register(Reminder, ReminderAdmin)
