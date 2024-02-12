from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from stakeholder.models import (
    UserRoleType,
    UserTitle,
    LoginStatus,
    Organisation,
    OrganisationUser,
    OrganisationRepresentative,
    OrganisationInvites,
    Reminders,
    UserProfile
)


class UserRoleTypeAdmin(admin.ModelAdmin):
    """Admin page for UserRoleType model

    """
    list_display = ("name", "description")
    search_fields = [
        "name",
        "description"
    ]


class UserTitleAdmin(admin.ModelAdmin):
    """Admin page for UserTitle model

    """
    list_display = ("id", "name")
    search_fields = ["name"]


class LoginStatusAdmin(admin.ModelAdmin):
    """Admin page for LoginStatus model

    """
    list_display = ("id", "name")
    search_fields = ["name"]


admin.site.register(UserRoleType, UserRoleTypeAdmin)
admin.site.register(UserTitle, UserTitleAdmin)
admin.site.register(LoginStatus, LoginStatusAdmin)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """Admin page for Organisation model

    """
    list_display = ("name", "short_code", "province", "national")
    search_fields = [
        "name",
        "province__name",
        "short_code",
    ]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    list_display = (
        "picture",
    )
    autocomplete_fields = ['current_organisation']


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrganisationPersonnelBaseAdmin(admin.ModelAdmin):
    list_display = ("get_user_first_name", "get_user_last_name",
                    "organisation")
    search_fields = [
        "user__first_name",
        "user__last_name",
        "organisation__name"
    ]
    autocomplete_fields = ["user", "organisation"]

    @admin.display(ordering='user__first_name', description='First Name')
    def get_user_first_name(self, obj):
        return obj.user.first_name if obj.user.first_name else '-'

    @admin.display(ordering='user__last_name', description='Last Name')
    def get_user_last_name(self, obj):
        return obj.user.last_name


@admin.register(OrganisationUser)
class OrganisationUserAdmin(OrganisationPersonnelBaseAdmin):
    """Admin page for OrganisationUser model

    """


@admin.register(OrganisationRepresentative)
class OrganisationRepresentativeAdmin(OrganisationPersonnelBaseAdmin):
    """Admin page for OrganisationRepresentative model

    """


@admin.register(OrganisationInvites)
class OrganisationInvitesAdmin(admin.ModelAdmin):
    """Admin page for OrganisationInvites model

    """
    list_display = (
        "email",
        "organisation",
        "user_role",
        "joined",
        "assigned_as"
    )
    search_fields = [
        "email",
        "organisation__name",
        "user_role__name",
        "assigned_as"
    ]
    autocomplete_fields = ["user", "organisation"]
    list_filter = ['assigned_as', 'joined']


@admin.register(Reminders)
class RemindersAdmin(admin.ModelAdmin):
    """Admin page for Reminders model

    """
    list_display = (
        "title",
        "user",
        "reminder",
        "date",
        "status",
        "type",
        "email_sent",
        "organisation"
    )
    search_fields = [
        "title",
        "user__username",
        "status",
        "organisation__name",
        "type"
    ]
