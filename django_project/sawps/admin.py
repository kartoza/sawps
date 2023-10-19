from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.db.models.signals import post_save
from django_otp.plugins.otp_static.models import StaticDevice

from sawps.models import ExtendedGroup, ExtendedGroupPermission, save_extended_group
from sawps.forms.group_forms import ExtendedGroupForm

from sawps.utils import disconnected_signal


class CustomStaticDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'confirmed')
    search_fields = ('user__username',)


# Ensure users go through the allauth workflow when logging into admin.
admin.site.login = staff_member_required(
    admin.site.login, login_url='/accounts/login')
# Run the standard admin set-up.
admin.autodiscover()


class ExtendedGroupInline(admin.StackedInline):
    model = ExtendedGroup
    can_delete = False
    verbose_name_plural = 'ExtendedGroup'
    list_display = (
        'description',
    )
    form = ExtendedGroupForm


class GroupAdmin(BaseGroupAdmin):

    def save_model(self, request, obj, form, change):
        with disconnected_signal(post_save, save_extended_group, Group):
            super().save_model(request, obj, form, change)

    inlines = (ExtendedGroupInline, )
    list_display = (
        'name',
        'get_description',
    )

    def get_description(self, obj: ExtendedGroup) -> str:
        """
        Retrieve description from the
        related ExtendedGroup model.
        """
        try:
            return obj.extended.description
        except ExtendedGroup.DoesNotExist:
            return "No description"

    get_description.short_description = 'Description'


@admin.register(ExtendedGroupPermission)
class ExtendedGroupPermissionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'allow_for_organisation_member',
        'allow_for_organisation_manager'
    ]

# Unregister the model if it's already registered
admin.site.unregister(StaticDevice)
admin.site.register(StaticDevice, CustomStaticDeviceAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
