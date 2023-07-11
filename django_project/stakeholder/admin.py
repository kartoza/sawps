from django.contrib import admin
from stakeholder.models import UserRoleType, UserTitle, LoginStatus, UserProfile, Organisation, OrganisationUser, OrganisationRepresentative, OrganisationInvites

admin.site.register(UserRoleType)
admin.site.register(UserTitle)
admin.site.register(LoginStatus)
admin.site.register(UserProfile)
admin.site.register(Organisation)

@admin.register(OrganisationUser)
class OrganisationUserAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation")

@admin.register(OrganisationRepresentative)
class OrganisationRepresentativeAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation")
    

@admin.register(OrganisationInvites)
class OrganisationInvitesAdmin(admin.ModelAdmin):
    list_display = ("email", "organisation", "user_role" ,"joined","assigned_as")

