from django.contrib import admin
from stakeholder import models as stakeholderModels

admin.site.register(stakeholderModels.UserTitle)
admin.site.register(stakeholderModels.UserRoleType)
admin.site.register(stakeholderModels.LoginStatus)
admin.site.register(stakeholderModels.UserLogin)
admin.site.register(stakeholderModels.UserProfile)
