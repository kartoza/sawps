# -*- coding: utf-8 -*-


"""Admin page for regulatory permit models.
"""
from django.contrib import admin
import regulatory_permit.models as regulatoryPermitModels

admin.site.register(regulatoryPermitModels.DataUsePermission)
