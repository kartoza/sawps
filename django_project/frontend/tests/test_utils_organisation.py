import os
from django.test import TestCase
import mock
from frontend.utils.organisation import get_abbreviation, get_organisation_ids
from stakeholder.factories import organisationUserFactory


class TestUtilsOrganisation(TestCase):

    def test_get_abbreviation_one_word(self):
        abbreviation = get_abbreviation('CapeVerdeNature')
        self.assertEqual(abbreviation, 'CA')

    def test_get_abbreviation_multiple_word(self):
        abbreviation = get_abbreviation('Cape Verde Nature')
        self.assertEqual(abbreviation, 'CVN')

    def test_get_organisation_ids(self):
        org_user = organisationUserFactory.create()
        ids = get_organisation_ids(org_user.user)
        self.assertEqual(len(ids), 1)
        self.assertEqual(ids[0], org_user.organisation.id)
