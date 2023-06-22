from rest_framework.test import APIRequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from stakeholder.models import Organisation
from frontend.utils.organisation import (
    CURRENT_ORGANISATION_ID_KEY,
    CURRENT_ORGANISATION_KEY
)


class OrganisationAPIRequestFactory(APIRequestFactory):

    def __init__(self, organisation: Organisation = None):
        self.organisation = organisation
        self.middleware = SessionMiddleware(lambda x: None)
        super().__init__()

    def process_session(self, request, organisation_id = None):
        self.middleware.process_request(request)
        org_id = organisation_id
        if org_id is None and self.organisation:
            org_id = self.organisation.id
        request.session[CURRENT_ORGANISATION_ID_KEY] = org_id
        request.session[CURRENT_ORGANISATION_KEY] = 'test_organisation'
        request.session.save()

    def get(self, path, data=None, organisation_id=None, **extra):
        request = super().get(path, data=data, **extra)
        self.process_session(request, organisation_id)
        return request

    def post(self, path, data=None, organisation_id=None,
             format=None, content_type=None, **extra):
        request = super().post(path, data=data, format=format,
                               content_type=content_type, **extra)
        self.process_session(request, organisation_id)
        return request
