from django.test import TestCase
from occurrence.models import SurveyMethod, SamplingSizeUnit
from occurrence.factories import SurveyMethodFactory, SamplingSizeUnitFactory
from django.db.utils import IntegrityError


class SurveyMethodTestCase(TestCase):
    """survey method test case"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.survey_method = SurveyMethodFactory()

    def test_create_survey_method(self):
        """test create survey method"""
        self.assertTrue(
            isinstance(self.survey_method, SurveyMethod)
        )
        self.assertEqual(SurveyMethod.objects.count(), 1)
        self.assertEqual(self.survey_method.name, 'survey method 0')

    def test_update_survey_method(self):
        """test update survey method"""
        self.survey_method.name = 'survey method 1'
        self.survey_method.save()
        self.assertEqual(
            SurveyMethod.objects.get(id=1).name,
            'survey method 1',
        )

    def test_survey_method_unique_name_constraint(self):
        """test survey method unique name constraint"""
        with self.assertRaises(Exception) as raised:
            OccurrenceFactories.SurveyMethodFactory(name='survey method 0')
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_survey_method_unique_sort_id_constraint(self):
        """test survey method unique sort id constraint"""
        with self.assertRaises(Exception) as raised:
            OccurrenceFactories.SurveyMethodFactory(sort_id=0)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_survey_method(self):
        """test delete survey method"""
        self.survey_method.delete()
        self.assertEqual(SurveyMethod.objects.count(), 0)


class SamplingSizeUnitTestCase(TestCase):
    """sampling size unit testcase"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.sampling_size_unit = SamplingSizeUnitFactory(unit='cm')

    def test_create_sampling_size_unit(self):
        """test create sampling size unit"""
        self.assertTrue(isinstance(self.sampling_size_unit, SamplingSizeUnit))
        self.assertEqual(SamplingSizeUnit.objects.count(), 1)
        self.assertEqual(self.sampling_size_unit.unit, 'cm')

    def test_update_sampling_size_unit(self):
        """test update sampling size unit"""
        self.sampling_size_unit.unit = 'mm'
        self.sampling_size_unit.save()
        self.assertEqual(SamplingSizeUnit.objects.get(id=1).unit, 'mm')

    def test_sampling_size_unit_unique_unit_constraint(self):
        """testing unique values for the unti"""
        with self.assertRaises(Exception) as raised:
            SamplingSizeUnitFactory(unit='mm')
            self.assertEqual(raised.exception, IntegrityError)

    def test_delete_sampling_size_unit(self):
        """test delete sampling size unit"""
        self.sampling_size_unit.delete()
        self.assertEqual(SamplingSizeUnit.objects.count(), 0)