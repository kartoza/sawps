from django.test import TestCase
from occurrence.models import (
    SurveyMethod, 
    SamplingSizeUnit, 
)
from occurrence.factories import SurveyMethodFactory
from occurrence.factories import SamplingSizeUnitFactory
from species.models import Taxon
from species.factories import TaxonRankFactory
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class SurveyMethodTestCase(TestCase):
    """Survey method test case."""

    @classmethod
    def setUpTestData(cls):
        """Setup test data."""
        cls.survey_method = SurveyMethodFactory()

    def test_create_survey_method(self):
        """Test create survey method."""
        self.assertTrue(
            isinstance(self.survey_method, SurveyMethod)
        )
        self.assertEqual(SurveyMethod.objects.count(), 1)
        self.assertEqual(self.survey_method.name, SurveyMethod.objects.get(id=self.survey_method.id).name)

    def test_update_survey_method(self):
        """Test update survey method."""
        self.survey_method.name = 'survey method 1'
        self.survey_method.save()
        self.assertEqual(
            SurveyMethod.objects.get(id=self.survey_method.id).name,
            'survey method 1',
        )

    def test_survey_method_unique_name_constraint(self):
        """Test survey method unique name constraint."""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(name='survey method 0')
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_survey_method_unique_sort_id_constraint(self):
        """Test survey method unique sort id constraint."""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(sort_id=0)
            self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_survey_method(self):
        """Test delete survey method."""
        self.survey_method.delete()
        self.assertEqual(SurveyMethod.objects.count(), 0)

        
class SamplingSizeUnitTestCase(TestCase):
    """Sampling size unit testcase."""

    @classmethod
    def setUpTestData(cls):
        """Setup test data."""
        cls.sampling_size_unit = SamplingSizeUnitFactory(unit='cm')

    def test_create_sampling_size_unit(self):
        """Test create sampling size unit."""
        self.assertTrue(isinstance(self.sampling_size_unit, SamplingSizeUnit))
        self.assertEqual(SamplingSizeUnit.objects.count(), 1)
        self.assertEqual(self.sampling_size_unit.unit, 'cm')

    def test_update_sampling_size_unit(self):
        """Test update sampling size unit."""
        self.sampling_size_unit.unit = 'mm'
        self.sampling_size_unit.save()
        self.assertEqual(SamplingSizeUnit.objects.get(id=self.sampling_size_unit.id).unit, 'mm')

    def test_sampling_size_unit_unique_unit_constraint(self):
        """Testing unique values for the unit."""
        with self.assertRaises(Exception) as raised:
            SamplingSizeUnitFactory(unit='mm')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_sampling_size_unit(self):
        """Test delete sampling size unit."""
        self.sampling_size_unit.delete()
        self.assertEqual(SamplingSizeUnit.objects.count(), 0)

