from django.contrib import admin
from stakeholder.models import UserRoleType, UserTitle, LoginStatus, UserProfile, Organisation, OrganisationUser, OrganisationRepresentative

admin.site.register(UserRoleType)
admin.site.register(UserTitle)
admin.site.register(LoginStatus)
admin.site.register(UserProfile)
admin.site.register(Organisation)
admin.site.register(OrganisationUser)
admin.site.register(OrganisationRepresentative)
