from django.test import TestCase
from occurrence.models import SurveyMethod, OccurrenceStatus
from occurrence.factories import SurveyMethodFactory, OccurrenceStatusFactory 
from django.db.utils import IntegrityError


class SurveyMethodTestCase(TestCase):
    """survey method test case"""

    @classmethod
    def setUpTestData(cls):
        """setup test data for survey method testcase"""
        cls.survey_method = SurveyMethodFactory()

    def test_create_survey_method(self):
        """test create survey method"""
        self.assertTrue(
            isinstance(self.survey_method, 
            SurveyMethod)
        )
        self.assertEqual(
            SurveyMethod.objects.count(), 1)
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
            SurveyMethodFactory(name='survey method 0')
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_survey_method_unique_sort_id_constraint(self):
        """test survey method unique sort id constraint"""
        with self.assertRaises(Exception) as raised:
            SurveyMethodFactory(sort_id=0)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_delete_survey_method(self):
        """test delete survey method"""
        self.survey_method.delete()
        self.assertEqual(
            SurveyMethod.objects.count(), 0)


class OccurrenceStatusTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setup test data for occurrence status testcase"""
        cls.occurrence_status = OccurrenceStatusFactory()
    
    def test_create_occurrence_status(self):
        """test create occurrence status"""
        self.assertTrue(
            isinstance(self.occurrence_status, 
            OccurrenceStatus)
        )
        self.assertEqual(
            OccurrenceStatus.objects.count(), 1)
        self.assertEqual(self.occurrence_status.name, 'occurrence status 0')    
    
    def test_update_occurrence_status(self):
        """ test update occurrence status"""
        self.occurrence_status.name = 'occurrence status 1'
        self.occurrence_status.save()
        self.assertEqual(
            OccurrenceStatus.objects.get(id=1).name,
            'occurrence status 1',
        )

    def test_occurrence_status_unique_name_constraint(self):
        """test occurrence status unique name constraint"""
        with self.assertRaises(Exception) as raised:
            OccurrenceStatusFactory(name='occurrence status 0')
        self.assertEqual(IntegrityError, type(raised.exception))


    def test_delete_occurrence_status(self):
        """test delete occurrence status"""
        self.occurrence_status.delete()
        self.assertEqual(
            OccurrenceStatus.objects.count(), 0)