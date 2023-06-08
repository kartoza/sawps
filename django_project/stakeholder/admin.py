from django.contrib import admin
from stakeholder.models import UserRoleType, UserTitle, LoginStatus, UserProfile

admin.site.register(UserRoleType)
admin.site.register(UserTitle)
admin.site.register(LoginStatus)
admin.site.register(UserProfile)
