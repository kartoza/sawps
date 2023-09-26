from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from sawps.models import ExtendedGroup
from django_otp.plugins.otp_static.models import StaticDevice


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


class GroupAdmin(BaseGroupAdmin):
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


admin.site.register(StaticDevice, CustomStaticDeviceAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
