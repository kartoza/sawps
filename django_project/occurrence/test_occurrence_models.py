from django.test import TestCase
import occurrence.models as OccurrenceModels
import occurrence.factories as OccurrenceFactories
from django.db.utils import IntegrityError


class SurveyMethodTestCase(TestCase):
    """survey method test case"""

    @classmethod
    def setUpTestData(cls):
        """setup test data"""
        cls.survey_method = OccurrenceFactories.SurveyMethodFactory()

    def test_create_survey_method(self):
        """test create survey method"""
        self.assertTrue(
            isinstance(self.survey_method, OccurrenceModels.SurveyMethod)
        )
        self.assertEqual(OccurrenceModels.SurveyMethod.objects.count(), 1)
        self.assertEqual(self.survey_method.name, 'survey method 0')

    def test_update_survey_method(self):
        """test update survey method"""
        self.survey_method.name = 'survey method 1'
        self.survey_method.save()
        self.assertEqual(
            OccurrenceModels.SurveyMethod.objects.get(id=1).name,
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
        self.assertEqual(OccurrenceModels.SurveyMethod.objects.count(), 0)
