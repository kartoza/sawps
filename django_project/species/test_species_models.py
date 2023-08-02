from rest_framework import status
from django.urls import reverse
import base64
from django.test import Client
from django.test import TestCase
from species.models import (
    TaxonRank, 
    Taxon, 
    OwnedSpecies, 
    TaxonSurveyMethod
)
from species.factories import (
    TaxonRankFactory,
    TaxonFactory,
    OwnedSpeciesFactory,
    TaxonSurveyMethodF
)
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from occurrence.models import SurveyMethod
from species.serializers import TaxonSerializer


class TaxonRankTestCase(TestCase):
    """Taxon rank test case."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for taxon rank test case."""
        cls.taxonRank = TaxonRankFactory()

    def test_create_taxon_rank(self):
        """Test create taxon rank."""
        self.assertTrue(isinstance(self.taxonRank, TaxonRank))
        self.assertEqual(
            self.taxonRank.name, 
            TaxonRank.objects.get(id=self.taxonRank.id).name
        )

    def test_update_taxon_rank(self):
        """Test update taxon rank."""
        self.taxonRank.name = 'taxon_rank_1'
        self.taxonRank.save()
        self.assertEqual(
            TaxonRank.objects.get(id=self.taxonRank.id).name, 
            'taxon_rank_1'
        )

    def test_unique_taxon_rank_name_constraint(self):
        """Test unique taxon rank name constraint."""
        with self.assertRaises(Exception) as raised:
            TaxonRankFactory(name='taxon_rank_1')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_taxon_rank(self):
        """Test delete taxon rank."""
        self.taxonRank.delete()
        self.assertEqual(TaxonRank.objects.count(), 0)


class TaxonTestCase(TestCase):
    """Taxon model test case."""
    @classmethod
    def setUpTestData(cls):
        """Taxon model test data."""
        cls.taxonRank = TaxonRankFactory.create(
            name='Species'
        )
        cls.taxon = TaxonFactory.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=cls.taxonRank,
        )
        cls.url = reverse('species')
        
    def test_get_taxon_list(self):
        """Taxon list API test"""

        user = User.objects.create_user(
            username='testuserd',
            password='testpasswordd'
        )
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +
            base64.b64encode(b'testuserd:testpasswordd').decode('ascii'),
        }
        client = Client()
        response = client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = TaxonSerializer([self.taxon], many=True).data
        self.assertEqual(expected_data, response.data)

    def test_create_taxon(self):
        """Test create taxon."""
        self.assertTrue(isinstance(self.taxon, Taxon))
        self.assertEqual(Taxon.objects.count(), 1)
        self.assertEqual(
            self.taxon.scientific_name, 
            Taxon.objects.get(id=self.taxon.id).scientific_name
        )

    def test_update_taxon(self):
        """Test update taxon objects."""
        self.taxon.scientific_name = 'taxon_1'
        self.taxon.infraspecific_epithet = 'infra_1'
        self.taxon.save()
        self.assertEqual(
            Taxon.objects.get(id=self.taxon.id).scientific_name, 
            'taxon_1'
        )
        self.assertEqual(
            Taxon.objects.get(id=self.taxon.id).infraspecific_epithet, 
            'infra_1'
        )

    def test_taxon_unique_scientific_name_constraint(self):
        """Test taxon unique scientific name constraint."""
        with self.assertRaises(Exception) as raised:
            Taxon.objects.create(
                scientific_name='taxon_1',
                common_name_varbatim='taxon_0',
                colour_variant=False,
                taxon_rank=self.taxonRank,
            )
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_taxon_unique_infraspecific_epithet_constraint(self):
        """Test taxon unique infraspecific epithet constraint."""
        with self.assertRaises(Exception) as raised:
            Taxon.objects.create(
                scientific_name='taxon_0',
                common_name_varbatim='taxon_0',
                colour_variant=False,
                infraspecific_epithet='infra_1',
                taxon_rank=self.taxonRank,
            )
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_taxon_relation_to_self(self):
        """Test taxon relation to self."""
        self.taxon2 = Taxon.objects.create(
            scientific_name='taxon_1',
            common_name_varbatim='taxon_1',
            colour_variant=False,
            taxon_rank=self.taxonRank,
            parent=self.taxon,
        )
        self.assertEqual(self.taxon2.parent, self.taxon)


    def test_delete_taxon(self):
        """Test delete taxon."""
        self.taxon.delete()
        self.assertEqual(Taxon.objects.count(), 0)
        """Test delete taxon rank."""
        self.taxonRank.delete()
        self.assertEqual(TaxonRank.objects.count(), 0)


class OwnedSpeciesTestCase(TestCase):
    """Owned species test case."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for owned species test case."""
        user = User.objects.create_user(username='testuser', password='12345')
        taxon = Taxon.objects.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=TaxonRankFactory(),
        )
        cls.ownedSpecies = OwnedSpeciesFactory(taxon=taxon, user=user)

    def test_create_owned_species(self):
        """Test create owned species."""
        self.assertTrue(isinstance(self.ownedSpecies, OwnedSpecies))
        self.assertEqual(OwnedSpecies.objects.count(), 1)

    def test_update_owned_species(self):
        """Test update owned species."""
        self.ownedSpecies.area_available_to_species = 45.67
        self.ownedSpecies.save()
        self.assertEqual(
            OwnedSpecies.objects.get(
            id=self.ownedSpecies.id).area_available_to_species, 
            45.67
        )

    def test_delete_owned_species(self):
        """Test delete owned species."""
        self.ownedSpecies.delete()
        self.assertEqual(OwnedSpecies.objects.count(), 0)


class TaxonSurveyMethodTestCase(TestCase):
    """Taxon survey method count test case."""
    @classmethod
    def setUpTestData(cls):
        """SetUpTestData for Taxon survey method count test case."""
        cls.taxon = Taxon.objects.create(
            scientific_name='taxon_0',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=TaxonRankFactory(),
        )
        cls.survey_method = SurveyMethod.objects.create(
            name='Unknown', 
            sort_id='1'
        )        
        cls.taxon_survey_method = TaxonSurveyMethodF(
            taxon=cls.taxon, 
            survey_method=cls.survey_method
        )
    
    def test_create_taxon_survey_method(self):
        """Test create Taxon survey method count."""
        self.assertTrue(
            isinstance(self.taxon_survey_method, TaxonSurveyMethod)
        )
        self.assertEqual(TaxonSurveyMethod.objects.count(), 1)
        self.assertEqual(
            TaxonSurveyMethod.objects.filter(
            taxon__scientific_name=self.taxon.scientific_name
            ).count(), 1
        )
        self.assertEqual(
            TaxonSurveyMethod.objects.filter(
            survey_method__name=self.survey_method.name
            ).count(), 1
        )

    def test_update_taxon_survey_method(self):
        """Test update Taxon survey method count."""
        taxon = TaxonFactory.create(
            scientific_name='taxon',
            common_name_varbatim='taxon_0',
            colour_variant=False,
            taxon_rank=TaxonRankFactory(),
        )
        self.taxon_survey_method.taxon = taxon
        self.taxon_survey_method.save()
        self.assertEqual(
            TaxonSurveyMethod.objects.filter(
            taxon__scientific_name='taxon').count(), 
            1
        )


    def test_delete_taxon_survey_method(self):
        """Test delete Taxon survey method count."""
        self.taxon.delete()
        self.assertEqual(TaxonSurveyMethod.objects.count(), 0)